#!/usr/bin/env python3
"""Check the package offline without changing files or host settings."""

import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AI_DOMAINS = {
    "chatgpt.com", "openai.com", "oaistatic.com", "oaiusercontent.com",
    "anthropic.com", "claude.ai", "lumo.proton.me", "x.ai",
}
SKILL_NAMES = ("lsrules-audit", "lsrules-source-review", "lsrules-release")
SKILL_SECTIONS = ("Prerequisites", "Constraints", "Instructions", "Verification", "Troubleshooting", "References")
SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
DAYBREAK_MODEL = "gpt-daybreak-blue-latest"
DAYBREAK_CONTRACT = ".agents/agents/daybreak-adversary.md"


def scalar(value):
    """Read the package's string-only frontmatter subset without YAML evaluation."""
    value = value.strip()
    if not value or value[0] in "!&*|>[{":
        raise ValueError("Frontmatter needs a single-line string scalar.")
    if value.startswith('"'):
        parsed = json.loads(value)
        if not isinstance(parsed, str):
            raise ValueError("Quoted frontmatter values must be strings.")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise ValueError("Unclosed frontmatter string.")
        return value[1:-1].replace("''", "'")
    return value


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Frontmatter must start on the first line.")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("Frontmatter has no closing delimiter.") from error
    result = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        nested = re.fullmatch(r"(?: {2}| {4})([a-z][a-z0-9_-]*):\s*(.+)", line)
        if nested and isinstance(result.get("metadata"), dict):
            name, value = nested.groups()
            if name in result["metadata"]:
                raise ValueError("Duplicate metadata key.")
            result["metadata"][name] = scalar(value)
            continue
        match = re.fullmatch(r"([a-z][a-z0-9-]*):\s*(.*)", line)
        if not match:
            raise ValueError("Unsupported frontmatter syntax.")
        name, value = match.groups()
        if name in result:
            raise ValueError("Duplicate frontmatter key.")
        result[name] = {} if name == "metadata" and not value else scalar(value)
    return result, "\n".join(lines[end + 1:])


def headings(text):
    result = []
    fence = None
    for index, line in enumerate(text.splitlines()):
        match = re.match(r"\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence:
            continue
        match = re.fullmatch(r"(#{1,6})\s+(.+?)\s*#*", line)
        if match:
            result.append((len(match.group(1)), match.group(2), index))
    return result


def skill_structure(name, body):
    found = headings(body)
    if [title for level, title, _ in found if level == 1] != [name]:
        return False
    sections = [title for level, title, _ in found if level == 2]
    if "Instructions" not in sections or len(sections) != len(set(sections)):
        return False
    if any(title not in SKILL_SECTIONS for title in sections):
        return False
    if sections != sorted(sections, key=SKILL_SECTIONS.index):
        return False
    current = None
    previous_level = 0
    lines = body.splitlines()
    for position, (level, title, line) in enumerate(found):
        if level > 3 or level > previous_level + 1:
            return False
        if level == 2:
            current = title
        if level == 3 and current not in {"Constraints", "Instructions", "Verification", "Troubleshooting"}:
            return False
        next_line = found[position + 1][2] if position + 1 < len(found) else len(lines)
        if level >= 2 and not any(value.strip() for value in lines[line + 1:next_line]):
            return False
        previous_level = level
    return True


def local_references_valid(path, root, skill_tree=None):
    text = path.read_text()
    targets = []
    for match in re.finditer(r"\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\)", text):
        targets.append((match.group(1) or match.group(2), False))
    for value in re.findall(r"`([^`\n]+)`", text):
        if " " not in value and (value.startswith((".agents/", ".codex/", "scripts/", "docs/", "rules/", "profiles/", "catalog/", "skills/", "agents/")) or value in {"AGENTS.md", "PUBLISHING.md"}):
            targets.append((value, True))
    for target, root_fallback in targets:
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https"}:
            continue
        if parsed.scheme or parsed.netloc:
            return False
        relative = unquote(parsed.path)
        if not relative:
            continue
        if Path(relative).is_absolute():
            return False
        candidates = [path.parent / relative]
        if root_fallback:
            candidates.append(root / relative)
        boundary = root if root_fallback else skill_tree or root
        if not any(candidate.resolve().is_relative_to(boundary.resolve()) and candidate.exists() for candidate in candidates):
            return False
    return True


def agent_checks(root):
    results = []

    def check(name, passed):
        results.append((name, bool(passed)))

    expected = [root / ".agents/skills" / name / "SKILL.md" for name in SKILL_NAMES]
    check("canonical_skill_files_present", all(path.is_file() for path in expected))
    for path, name in zip(expected, SKILL_NAMES):
        if not path.is_file():
            continue
        try:
            text = path.read_text()
            data, body = frontmatter(text)
            description = data.get("description", "")
            check(f"{name}_canonical_frontmatter", set(data).issubset(SKILL_FIELDS) and data.get("name") == name and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and isinstance(description, str) and 0 < len(description) < 1024 and "USE WHEN" in description and "NOT FOR" in description and bool(data.get("compatibility")))
            check(f"{name}_canonical_sections", skill_structure(name, body))
            check(f"{name}_bounded_static_entrypoint", len(text.splitlines()) <= 100 and not re.search(r"!`|(?m:^\s*@\S+)", body))
            check(f"{name}_local_references", local_references_valid(path, root, path.parent))
        except (OSError, ValueError, TypeError):
            check(f"{name}_readable_frontmatter", False)
    contract = root / DAYBREAK_CONTRACT
    try:
        data, body = frontmatter(contract.read_text())
        check("daybreak_contract_identity", set(data).issubset({"name", "description", "model"}) and data.get("name") == "daybreak-adversary" and bool(data.get("description")) and data.get("model") == DAYBREAK_MODEL)
        check("daybreak_contract_sections", len([x for x in headings(body) if x[0] == 1]) == 1 and {"Scope", "Review method", "Output", "Dispatch"}.issubset({x[1] for x in headings(body) if x[0] == 2}))
    except (OSError, ValueError, TypeError):
        check("daybreak_contract_readable", False)
    adapter = root / ".codex/agents/daybreak-adversary.toml"
    try:
        data = tomllib.loads(adapter.read_text())
        check("codex_adapter_fields_allowlisted", set(data) == {"name", "description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions"})
        check("codex_adapter_required_metadata", data.get("name") == "daybreak_adversary" and bool(data.get("description")) and bool(data.get("developer_instructions")))
        check("codex_adapter_daybreak_read_only", data.get("model") == DAYBREAK_MODEL and data.get("model_reasoning_effort") == "high" and data.get("sandbox_mode") == "read-only")
        check("codex_adapter_canonical_contract_reference", DAYBREAK_CONTRACT in data.get("developer_instructions", "") and contract.is_file())
    except (OSError, ValueError, TypeError):
        check("codex_adapter_readable", False)
    documents = [root / "AGENTS.md", root / ".agents/README.md", contract, root / "README.md", root / "PUBLISHING.md", *sorted((root / ".agents/rules").glob("*.md"))]
    check("agent_rules_present", len(list((root / ".agents/rules").glob("*.md"))) >= 3)
    check("agent_document_headings", all(path.is_file() and len([x for x in headings(path.read_text()) if x[0] == 1]) == 1 for path in documents))
    check("agent_document_local_references", all(path.is_file() and local_references_valid(path, root) for path in documents))
    return results


def domains_overlap(left, right):
    left = left.lower().rstrip(".")
    right = right.lower().rstrip(".")
    return left == right or left.endswith("." + right) or right.endswith("." + left)


def main():
    failures = []
    checks = []

    def check(name, passed):
        checks.append(name)
        if not passed:
            failures.append(name)

    def read(name):
        return json.loads((ROOT / name).read_text())

    domains = read("rules/work-domains.json")
    profiles = read("profiles/policy.json")
    catalog = read("catalog/blocklists.json")
    example = read("rules/global-focus-disabled.lsrules")
    values = domains["domains"]
    check("twelve_unique_domains", len(values) == len(set(values)) == 12)
    check("domain_syntax", all(re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", value) for value in values))
    check("required_ai_services_not_in_focus_denies",
          not any(domains_overlap(value, required) for value in values for required in REQUIRED_AI_DOMAINS))
    check("manual_work_source", domains.get("native_import_format") is False and domains.get("profile_name") == "Work")
    check("profile_metadata_never_auto_applies", profiles.get("native_import_format") is False and profiles.get("automatic_apply") is False)
    check("catalog_never_fetches_or_applies", catalog.get("automatic_fetch") is False and catalog.get("automatic_apply") is False)
    check("no_upstream_contents_vendored", catalog.get("upstream_list_contents_vendored") is False)
    rules = example.get("rules", [])
    check("one_portable_rule", len(rules) == 1)
    if rules:
        rule = rules[0]
        check("portable_rule_starts_disabled", rule.get("disabled") is True)
        check("portable_rule_denies_outgoing", rule.get("action") == "deny" and rule.get("direction") == "outgoing")
        check("portable_rule_any_process_high_priority", rule.get("process") == "any" and rule.get("priority") == "high")
        check("portable_domains_match_manual_source", sorted(rule.get("remote-domains", [])) == sorted(values))
        check("no_undocumented_native_profile_field", "profile" not in rule and "profile" not in example)
        selectors = {"remote", "remote-addresses", "remote-hosts", "remote-domains"}
        check("one_native_remote_selector", len(selectors.intersection(rule)) == 1)
        check("documented_native_fields_only", set(rule).issubset({"process", "action", "direction", "priority", "disabled", "remote-domains"}))
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.relative_to(ROOT).parts and "__pycache__" not in path.relative_to(ROOT).parts]
    check("no_machine_backups_or_captures", all(path.suffix not in {".lsbackup", ".pcap", ".pcapng"} and not path.name.endswith(".inventory.json") for path in files))
    contents = "\n".join(path.read_text() for path in files)
    check("no_private_user_paths", not re.search(r"/" + r"Users/[^/\s]+/", contents))
    check("no_literal_ip_addresses", not re.search(r"(?<![A-Za-z0-9])(?:\d{1,3}\.){3}\d{1,3}(?![A-Za-z0-9])", contents))
    check("no_executable_fingerprints", not re.search(r"(?<![A-Za-z0-9])[a-f0-9]{64}(?![A-Za-z0-9])", contents))
    check("no_private_vpn_server_labels", not re.search(r"\b[A-Z]{2}#\d+\b", contents))
    check("no_credential_bearing_urls", not re.search(r"https?://[^\s\"<>]+(?:[?&](?:token|authkey|api_key|key)=|@)", contents, re.IGNORECASE))
    for name, passed in agent_checks(ROOT):
        check(name, passed)
    print(json.dumps({"checks_passed": len(checks) - len(failures), "checks_total": len(checks), "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
