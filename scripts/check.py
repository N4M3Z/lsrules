#!/usr/bin/env python3
"""Check the package offline without changing files or host settings."""

import hashlib
import ipaddress
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AI_DOMAINS = {
    "chatgpt.com", "openai.com", "oaistatic.com", "oaiusercontent.com",
    "anthropic.com", "claude.ai", "lumo.proton.me", "x.ai",
}
FINGERPRINT = re.compile(r"(?<![A-Za-z0-9])[a-f0-9]{64}(?![A-Za-z0-9])")
IPV6_CANDIDATE = re.compile(
    r"(?<!\w)[0-9A-Fa-f:.]*:[0-9A-Fa-f:.]+(?:%[A-Za-z0-9_.~-]+)?(?!\w)"
)
PRIVATE_SUBMODULE_CONFIG = (
    '[submodule "lsrules-private"]\n'
    '\tpath = private\n'
    '\turl = https://github.com/N4M3Z/lsrules-private.git\n'
)
DOCUMENT_NAME = r"[A-Z][A-Z0-9]*-[0-9]{4} [A-Za-z0-9][A-Za-z0-9 ()_-]*\.md"
DOCUMENT_URL = r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/blob/[A-Za-z0-9_./%+-]+\.md"
DOCUMENT_DIGEST = r"[a-f0-9]{64}"
REPLACEMENT_RECORD = re.compile(
    rf"        - block: (?P<document>{DOCUMENT_NAME}):(?P<block>[1-9][0-9]*)\n"
    rf"          sha256: (?P<digest>{DOCUMENT_DIGEST})\n"
    rf"          path: replacements/(?P<path_digest>{DOCUMENT_DIGEST})\n"
)
# Accept only the existing adopt/v1 emitter shape, not general YAML syntax.
DOCUMENT_PROVENANCE = re.compile(
    "provenance:\n"
    "  _type: https://in-toto.io/Statement/v1\n"
    "  predicateType: https://slsa.dev/provenance/v1\n"
    "  subject:\n"
    rf"  - name: (?P<subject>docs/decisions/{DOCUMENT_NAME})\n"
    "    digest:\n"
    rf"      sha256: (?P<subject_digest>{DOCUMENT_DIGEST})\n"
    "  predicate:\n"
    "    buildDefinition:\n"
    "      buildType: adopt/v1\n"
    "      externalParameters:\n"
    "        source: ''\n"
    rf"        upstream_url: (?P<upstream_url>{DOCUMENT_URL})\n"
    "        upstream_commit: ''\n"
    "        transforms_applied:\n"
    "        - align\n"
    "      resolvedDependencies:\n"
    "      - name: upstream\n"
    rf"        uri: (?P<upstream_uri>{DOCUMENT_URL})\n"
    "        digest:\n"
    rf"          sha256: (?P<upstream_digest>{DOCUMENT_DIGEST})\n"
    "    runDetails:\n"
    "      builder:\n"
    "        id: rune-cli\n"
    "        version:\n"
    r"          rune: [0-9]+\.[0-9]+\.[0-9]+\n"
    "      metadata:\n"
    r"        startedOn: (?P<started>[0-9T:.+-]+)\n"
    "        review: reviewed\n"
    r"        reviewer: (?P<reviewer>[^\n]+)\n"
    r"        completedOn: (?P<completed>[0-9T:.+-]+)\n"
    r"        summary: [0-9]+ keep, [0-9]+ adapt\n"
    "        replacements:\n"
    rf"(?P<replacements>(?:        - block: {DOCUMENT_NAME}:[1-9][0-9]*\n"
    rf"          sha256: {DOCUMENT_DIGEST}\n"
    rf"          path: replacements/{DOCUMENT_DIGEST}\n){{1,64}})"
)


def regular_document_path(path, root):
    """Require a regular package file with no symlink path component."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    if any(part in {".", ".."} for part in relative.parts):
        return False
    if any((root / Path(*relative.parts[:index])).is_symlink()
           for index in range(1, len(relative.parts) + 1)):
        return False
    return path.is_file() and path.resolve().is_relative_to(root.resolve())


def document_bytes_match(path, root, digest):
    """Verify the digest of regular UTF-8 text inside the package."""
    if not regular_document_path(path, root):
        return False
    data = path.read_bytes()
    data.decode("utf-8")
    return b"\0" not in data and hashlib.sha256(data).hexdigest() == digest


def verified_provenance_text(path, text, root):
    """Mask only digest occurrences verified against their local document bytes."""
    if any((ord(character) < 32 and character != "\n")
           or 127 <= ord(character) <= 159 or character in "\u2028\u2029"
           for character in text):
        return False, text
    match = DOCUMENT_PROVENANCE.fullmatch(text)
    if not match or not regular_document_path(path, root):
        return False, text
    subject = Path(match["subject"])
    if path != root / "docs/decisions/.provenance" / (subject.name + ".yaml"):
        return False, text
    if match["upstream_url"] != match["upstream_uri"]:
        return False, text
    try:
        started = datetime.fromisoformat(match["started"])
        completed = datetime.fromisoformat(match["completed"])
        if started.utcoffset() is None or completed.utcoffset() is None or completed < started:
            return False, text
    except ValueError:
        return False, text
    reviewer = match["reviewer"]
    if (not reviewer[0].isalpha()
            or reviewer.lower() in {"null", "true", "false", "yes", "no", "on", "off"}
            or re.search(r":\s|(?:^|\s)#", reviewer)
            or scalar(reviewer) != reviewer):
        return False, text
    references = [
        (root / subject, match["subject_digest"]),
        (path.parent / "sources" / match["upstream_digest"], match["upstream_digest"]),
    ]
    spans = [match.span("subject_digest"), match.span("upstream_digest")]
    blocks = set()
    offset = match.start("replacements")
    for replacement in REPLACEMENT_RECORD.finditer(match["replacements"]):
        if (replacement["document"] != subject.name or replacement["block"] in blocks
                or replacement["digest"] != replacement["path_digest"]):
            return False, text
        blocks.add(replacement["block"])
        references.append((path.parent / "replacements" / replacement["digest"], replacement["digest"]))
        spans.extend((offset + start, offset + end)
                     for start, end in (replacement.span("digest"), replacement.span("path_digest")))
    if not all(document_bytes_match(document, root, digest) for document, digest in references):
        return False, text
    for start, end in sorted(spans, reverse=True):
        text = text[:start] + " " * (end - start) + text[end:]
    return True, text


def scalar(value):
    """Read a provenance string without YAML evaluation."""
    value = value.strip()
    if not value or value[0] in "!&*|>[{":
        raise ValueError("Provenance needs a single-line string scalar.")
    if value.startswith('"'):
        parsed = json.loads(value)
        if not isinstance(parsed, str):
            raise ValueError("Quoted provenance values must be strings.")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise ValueError("Unclosed provenance string.")
        return value[1:-1].replace("''", "'")
    return value


def local_references_valid(path, root):
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
        private_parts = tuple(part.casefold() for part in Path(os.path.abspath(root / "private")).parts)
        for candidate in candidates:
            parts = []
            for part in candidate.absolute().parts:
                if part == "..":
                    parts = parts[:-1]
                elif part != ".":
                    parts.append(part.casefold())
                if tuple(parts) == private_parts:
                    return False
        boundary = root
        if not any(candidate.resolve().is_relative_to(boundary.resolve()) and candidate.exists() for candidate in candidates):
            return False
    return True


def document_checks(root):
    """Check local links in the maintained guides without a prose toolchain."""
    names = (
        "README.md", "INSTALL.md", "AGENTS.md", "CONTRIBUTING.md", "PUBLISHING.md",
        "THIRD_PARTY.md", "docs/reference.md", "docs/private-companion.md",
        "docs/skeleton-alignment.md", "docs/native-workflow.md",
        "docs/cleanup-method.md", "docs/identities.md",
    )
    return [("document_local_references", all(
        (root / name).is_file() and local_references_valid(root / name, root)
        for name in names
    ))]


def domains_overlap(left, right):
    left = left.lower().rstrip(".")
    right = right.lower().rstrip(".")
    return left == right or left.endswith("." + right) or right.endswith("." + left)


def contains_literal_ip_address(text):
    """Recognize address literals without resolving names or checking networks."""
    if re.search(r"(?<![A-Za-z0-9])(?:\d{1,3}\.){3}\d{1,3}(?![A-Za-z0-9])", text):
        return True
    for match in IPV6_CANDIDATE.finditer(text):
        value = match.group().strip(".")
        candidates = [value]
        if value.endswith(":"):
            candidates.append(value[:-1])
        for candidate in candidates:
            try:
                ipaddress.IPv6Address(candidate)
            except ValueError:
                continue
            return True
    return False


def publication_entries(root):
    """List public entries without descending into the reserved private boundary."""
    result = []

    def visit(directory):
        for path in directory.iterdir():
            if directory == root and path.name in {".git", ".jj"}:
                continue
            if path.name == "__pycache__":
                continue
            result.append(path)
            if path == root / "private" or path.name in {".git", ".jj"}:
                continue
            if not path.is_symlink() and path.is_dir():
                visit(path)

    visit(root)
    return result


def read_only_git(directory, arguments):
    """Read local Git evidence without hooks, network transports, or optional locks."""
    if tuple(arguments) not in {
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "--verify", "HEAD^{commit}"),
        ("ls-files", "--stage", "-z", "--", "private"),
    }:
        return None
    environment = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    environment.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_NO_LAZY_FETCH": "1",
    })
    try:
        # The command uses the fixed local Git probe allowlist above.
        result = subprocess.run(  # noqa: S603
            ["git", "-c", "core.fsmonitor=false", "-c", "protocol.allow=never",  # noqa: S607
             "-C", str(directory), *arguments],
            env=environment, capture_output=True, text=True, check=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return None
    return result.stdout if len(result.stdout) <= 4096 else None


def git_metadata_is_local(directory):
    """Reject redirects and symlinks in metadata used by the approved Git probes."""
    try:
        for name in ("refs", "objects", "reftable"):
            pending = [directory / name]
            while pending:
                path = pending.pop()
                if path.is_symlink():
                    return False
                if not path.exists():
                    continue
                if path.is_dir():
                    pending.extend(path.iterdir())
                elif not path.is_file():
                    return False
        for name in ("commondir", "objects/info/alternates", "objects/info/http-alternates"):
            path = directory / name
            if path.is_symlink() or path.exists():
                return False
        for name in ("HEAD", "index", "packed-refs", "shallow", "config", "config.worktree"):
            path = directory / name
            if path.is_symlink() or (path.exists() and not path.is_file()):
                return False
            if name.startswith("config") and path.exists():
                if re.search(r"(?im)^\s*\[\s*include", path.read_text()):
                    return False
    except (OSError, UnicodeError):
        return False
    return True


def private_submodule_valid(root):
    """Validate the one private boundary without reading its payload."""
    config = root / ".gitmodules"
    private = root / "private"
    if config.is_symlink() or private.is_symlink():
        return False
    if not config.exists():
        return not private.exists()
    if not regular_document_path(config, root) or config.read_bytes() != PRIVATE_SUBMODULE_CONFIG.encode():
        return False
    if not private.exists():
        return True
    if private.is_symlink() or not private.is_dir():
        return False
    with os.scandir(private) as children:
        if next(children, None) is None:
            return True
    marker = private / ".git"
    if not regular_document_path(marker, root):
        return False
    if marker.read_bytes() != b"gitdir: ../.git/modules/lsrules-private\n":
        return False
    git_directory = root / ".git/modules/lsrules-private"
    for path in (root / ".git", root / ".git/modules", git_directory):
        if path.is_symlink() or not path.is_dir():
            return False
    if not all(git_metadata_is_local(path) for path in (root / ".git", git_directory)):
        return False
    parent_top_level = read_only_git(root, ["rev-parse", "--show-toplevel"])
    if parent_top_level != str(root.resolve()) + "\n":
        return False
    top_level = read_only_git(private, ["rev-parse", "--show-toplevel"])
    if top_level != str(private.resolve()) + "\n":
        return False
    head = read_only_git(private, ["rev-parse", "--verify", "HEAD^{commit}"])
    if head is None or not re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})\n", head):
        return False
    index = read_only_git(root, ["ls-files", "--stage", "-z", "--", "private"])
    return index == f"160000 {head.strip()} 0\tprivate\0"


def main():
    failures = []
    checks = []

    def check(name, passed):
        checks.append(name)
        if not passed:
            failures.append(name)

    def read(name):
        return json.loads((ROOT / name).read_text())

    def finish():
        print(json.dumps({"checks_passed": len(checks) - len(failures), "checks_total": len(checks), "failures": failures}, indent=2))
        return 1 if failures else 0

    entries = publication_entries(ROOT)
    check("no_package_symlinks", all(not path.is_symlink() for path in entries))
    check("no_unexpected_repository_metadata", all(
        path.name not in {".git", ".jj"}
        and (path.name != ".gitmodules" or path == ROOT / ".gitmodules")
        for path in entries
    ))
    if failures:
        return finish()
    check("private_submodule_boundary_verified", private_submodule_valid(ROOT))
    if failures:
        return finish()

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
    files = [path for path in entries if path != ROOT / "private" and path.is_file()]
    check("no_machine_backups_or_captures", all(path.suffix not in {".lsbackup", ".pcap", ".pcapng"} and not path.name.endswith(".inventory.json") for path in files))
    texts = {path: path.read_text() for path in files}
    contents = "\n".join(texts.values())
    fingerprint_texts = []
    provenance_valid = True
    for path, text in texts.items():
        if path.parent == ROOT / "docs/decisions/.provenance" and path.suffix == ".yaml":
            try:
                valid, text = verified_provenance_text(path, text, ROOT)
            except (OSError, ValueError):
                valid = False
            provenance_valid = provenance_valid and valid
        fingerprint_texts.append(text)
    check("document_provenance_bytes_verified", provenance_valid)
    check("no_private_user_paths", not re.search(r"/" + r"Users/[^/\s]+/", contents))
    check("no_literal_ip_addresses", not contains_literal_ip_address(contents))
    check("no_executable_fingerprints", not FINGERPRINT.search("\n".join(fingerprint_texts)))
    check("no_private_vpn_server_labels", not re.search(r"\b[A-Z]{2}#\d+\b", contents))
    check("no_credential_bearing_urls", not re.search(r"https?://[^\s\"<>]+(?:[?&](?:token|authkey|api_key|key)=|@)", contents, re.IGNORECASE))
    for name, passed in document_checks(ROOT):
        check(name, passed)
    return finish()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        raise SystemExit(1) from None
