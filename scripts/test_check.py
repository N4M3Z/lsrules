#!/usr/bin/env python3
"""Exercise unsafe near misses without changing package files."""

import hashlib
import json
import os
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import check


def provenance_fixture():
    """Build public synthetic documents and their exact adoption record."""
    subject = b"# Synthetic decision\n\nA local decision.\n"
    upstream = b"# Synthetic source\n\nAn upstream decision.\n"
    replacement = b"A reviewed replacement.\n"
    def digest(data):
        return hashlib.sha256(data).hexdigest()

    name = "LSR-0002 Synthetic Decision.md"
    record_name = f"docs/decisions/.provenance/{name}.yaml"
    record = f"""provenance:
  _type: https://in-toto.io/Statement/v1
  predicateType: https://slsa.dev/provenance/v1
  subject:
  - name: docs/decisions/{name}
    digest:
      sha256: {digest(subject)}
  predicate:
    buildDefinition:
      buildType: adopt/v1
      externalParameters:
        source: ''
        upstream_url: https://github.com/example/documents/blob/main/docs/CORE-0002.md
        upstream_commit: ''
        transforms_applied:
        - align
      resolvedDependencies:
      - name: upstream
        uri: https://github.com/example/documents/blob/main/docs/CORE-0002.md
        digest:
          sha256: {digest(upstream)}
    runDetails:
      builder:
        id: rune-cli
        version:
          rune: 0.5.0
      metadata:
        startedOn: 2026-09-20T22:21:20.936339+00:00
        review: reviewed
        reviewer: Example Reviewer <reviewer@example.org>
        completedOn: 2026-09-20T22:21:21.171453+00:00
        summary: 1 keep, 1 adapt
        replacements:
        - block: {name}:1
          sha256: {digest(replacement)}
          path: replacements/{digest(replacement)}
"""
    return record_name, {
        record_name: record.encode(),
        f"docs/decisions/{name}": subject,
        f"docs/decisions/.provenance/sources/{digest(upstream)}": upstream,
        f"docs/decisions/.provenance/replacements/{digest(replacement)}": replacement,
    }


class PackageContentChecks(unittest.TestCase):
    def package_results(self, extra_files, symlinks=None, directories=(), git_reader=None, guard_private=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("rules/work-domains.json", "profiles/policy.json",
                         "catalog/blocklists.json", "rules/global-focus-disabled.lsrules"):
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((check.ROOT / name).read_bytes())
            for name, data in extra_files.items():
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
            for name in directories:
                (root / name).mkdir(parents=True, exist_ok=True)
            for name, target in (symlinks or {}).items():
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.is_file():
                    destination.unlink()
                destination.symlink_to(root / target)
            output = StringIO()
            with ExitStack() as stack:
                stack.enter_context(patch.object(check, "ROOT", root))
                stack.enter_context(patch.object(check, "agent_checks", return_value=[]))
                stack.enter_context(redirect_stdout(output))
                if git_reader is not None:
                    stack.enter_context(patch.object(check, "read_only_git", side_effect=git_reader))
                if guard_private:
                    for method in ("read_bytes", "read_text", "iterdir"):
                        original = getattr(Path, method)

                        def guarded(path, *args, _method=method, _original=original, **kwargs):
                            if path.is_relative_to(root / "private") and path != root / "private/.git":
                                raise AssertionError("Private payload was traversed or read.")
                            return _original(path, *args, **kwargs)

                        stack.enter_context(patch.object(Path, method, guarded))
                status = check.main()
            return status, json.loads(output.getvalue())

    def test_version_control_and_bytecode_binaries_are_not_package_content(self):
        status, result = self.package_results({
            ".git/objects/example": b"\x8b\x00",
            ".jj/repo/store/example": b"\x8b\x00",
            "scripts/__pycache__/example.pyc": b"\x8b\x00",
        })
        self.assertEqual(status, 0)
        self.assertEqual(result["failures"], [])

    def test_nested_repositories_fail_before_their_content_is_read(self):
        private_path = "/" + "Users/" + "example/config"
        for directory in (".git", ".jj"):
            with self.subTest(directory=directory):
                with patch.object(Path, "read_text", side_effect=AssertionError("Nested repository content was read.")):
                    status, result = self.package_results({
                        f"docs/{directory}/capture.lsbackup": private_path.encode(),
                    })
                self.assertEqual(status, 1)
                self.assertIn("no_unexpected_repository_metadata", result["failures"])

    def test_hidden_agent_content_still_receives_privacy_checks(self):
        private_path = "/" + "Users/" + "example/config"
        address = ".".join(("192", "0", "2", "7"))
        status, result = self.package_results({
            ".agents/rules/example.md": private_path.encode(),
            ".codex/agents/example.toml": address.encode(),
        })
        self.assertEqual(status, 1)
        self.assertIn("no_private_user_paths", result["failures"])
        self.assertIn("no_literal_ip_addresses", result["failures"])

    def test_ipv6_literals_are_rejected_in_public_and_hidden_text(self):
        colon = ":"
        compressed = colon.join(("2001", "db8", "", "7"))
        mapped = colon * 2 + "ffff" + colon + ".".join(("192", "0", "2", "7"))
        scoped = colon.join(("fe80", "", "1"))
        cases = [
            compressed,
            colon.join(("2001", "0DB8", "0001", "0002", "0003", "0004", "0005", "0006")),
            colon * 2,
            colon * 2 + "1",
            colon.join(("fd00", "", "5")),
            mapped,
            scoped + "%en0",
            f"https://[{compressed}]:443/path",
            f"https://[{scoped}%25en0]:443/path",
            f"({compressed}).",
            f"Endpoint {compressed}: blocked",
            colon.join(("2001", "db8", "", "")) + ": blocked",
            compressed + "/64",
        ]
        for value in cases:
            for name in ("docs/example.md", ".agents/notes.md"):
                with self.subTest(value=value, name=name):
                    status, result = self.package_results({name: value.encode()})
                    self.assertEqual(status, 1)
                    self.assertIn("no_literal_ip_addresses", result["failures"])

    def test_ipv6_detection_accepts_ordinary_colon_time_and_version_text(self):
        text = "\n".join([
            "Note: review the package.",
            "Time 12:34:56 and UTC+02:00.",
            "2026-10-17T12:34:56.123456+02:00",
            "Version 3.11.2 and https://example.org:443/path",
            "sha256: a reviewed document digest",
            "module" + ":" * 2 + "member",
            "abc:def and name:value",
        ])
        status, result = self.package_results({"docs/example.md": text.encode()})
        self.assertEqual(status, 0)
        self.assertNotIn("no_literal_ip_addresses", result["failures"])

    def test_only_root_submodule_metadata_is_supported(self):
        status, result = self.package_results({"docs/.gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode()})
        self.assertEqual(status, 1)
        self.assertIn("no_unexpected_repository_metadata", result["failures"])

    def test_uninitialized_private_declaration_needs_no_git(self):
        for directories in ((), ("private",)):
            with self.subTest(directories=directories):
                status, result = self.package_results({
                    ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode(),
                }, directories=directories, git_reader=lambda *_: self.fail("Uninitialized state invoked Git."))
                self.assertEqual(status, 0)
                self.assertEqual(result["failures"], [])

    def test_private_declaration_rejects_other_configuration(self):
        original = check.PRIVATE_SUBMODULE_CONFIG
        cases = [
            original.replace('"lsrules-private"', '"other"'),
            original.replace("path = private", "path = elsewhere"),
            original.replace("path = private", "path = ../private"),
            original.replace("N4M3Z/lsrules-private.git", "example/other.git"),
            original + "\tbranch = main\n",
            original + "\tpath = private\n",
            original + '[submodule "other"]\n\tpath = other\n',
            original + "[include]\n\tpath = other\n",
        ]
        for edited in cases:
            with self.subTest(edited=edited):
                status, result = self.package_results({".gitmodules": edited.encode()})
                self.assertEqual(status, 1)
                self.assertIn("private_submodule_boundary_verified", result["failures"])

    def test_private_directory_cannot_hide_ordinary_files(self):
        cases = [
            {"private/note": b"data"},
            {"private/note": b"data", ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode()},
            {"private/.git": b"gitdir: ../../elsewhere\n", ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode()},
            {"private/.git": b"gitdir: ../.git/modules/lsrules-private\n", ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode()},
            {"private": b"not a directory", ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode()},
        ]
        for files in cases:
            with self.subTest(files=list(files)):
                status, result = self.package_results(files, git_reader=lambda *_: self.fail("Invalid boundary invoked Git."))
                self.assertEqual(status, 1)
                self.assertIn("private_submodule_boundary_verified", result["failures"])

    def test_private_root_symlink_is_rejected_even_when_broken(self):
        for target, directories in (("elsewhere", ("elsewhere",)), ("missing", ())):
            with self.subTest(target=target):
                status, result = self.package_results({
                    ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode(),
                }, symlinks={"private": target}, directories=directories)
                self.assertEqual(status, 1)
                self.assertIn("no_package_symlinks", result["failures"])

    @staticmethod
    def valid_submodule_git(directory, arguments):
        commit = "a" * 40
        if arguments == ["rev-parse", "--show-toplevel"]:
            return str(directory.resolve()) + "\n"
        if arguments == ["rev-parse", "--verify", "HEAD^{commit}"]:
            return commit + "\n"
        if arguments == ["ls-files", "--stage", "-z", "--", "private"]:
            return f"160000 {commit} 0\tprivate\0"
        raise AssertionError("Unexpected Git command.")

    def test_initialized_private_payload_is_never_traversed(self):
        status, result = self.package_results({
            ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode(),
            "private/.git": b"gitdir: ../.git/modules/lsrules-private\n",
            "private/capture.lsbackup": b"\x8b\x00",
        }, directories=(".git/modules/lsrules-private",),
            symlinks={"private/linked-payload": "missing"},
            git_reader=self.valid_submodule_git, guard_private=True)
        self.assertEqual(status, 0)
        self.assertEqual(result["failures"], [])

    def test_initialized_private_boundary_needs_exact_git_evidence(self):
        commit = "a" * 40
        cases = [
            ("parent", "/unexpected\n"),
            ("top", "/unexpected\n"),
            ("head", None),
            ("head", "not a commit\n"),
            ("index", None),
            ("index", f"100644 {commit} 0\tprivate\0"),
            ("index", f"160000 {'b' * 40} 0\tprivate\0"),
            ("index", f"160000 {commit} 1\tprivate\0"),
            ("index", f"160000 {commit} 0\telsewhere\0"),
            ("index", f"160000 {commit} 0\tprivate\0" * 2),
        ]
        for kind, value in cases:
            def reader(directory, arguments, kind=kind, value=value):
                selected = "top" if "--show-toplevel" in arguments else "head" if "--verify" in arguments else "index"
                if selected == "top" and directory.name != "private":
                    selected = "parent"
                return value if selected == kind else self.valid_submodule_git(directory, arguments)

            with self.subTest(kind=kind, value=value):
                status, result = self.package_results({
                    ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode(),
                    "private/.git": b"gitdir: ../.git/modules/lsrules-private\n",
                }, directories=(".git/modules/lsrules-private",), git_reader=reader)
                self.assertEqual(status, 1)
                self.assertIn("private_submodule_boundary_verified", result["failures"])

    def test_private_git_metadata_cannot_redirect_through_symlinks(self):
        cases = [
            ({".git": "metadata"}, ("metadata/modules/lsrules-private",)),
            ({".git/modules": "metadata"}, (".git", "metadata/lsrules-private")),
            ({".git/modules/lsrules-private": "metadata"}, (".git/modules", "metadata")),
            ({"private/.git": "git-marker"}, (".git/modules/lsrules-private",)),
            ({".git/config": "git-marker"}, (".git/modules/lsrules-private",)),
            ({".git/modules/lsrules-private/refs/heads/main": "git-marker"}, (".git/modules/lsrules-private/refs/heads",)),
        ]
        for symlinks, directories in cases:
            with self.subTest(symlinks=symlinks):
                status, result = self.package_results({
                    ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode(),
                    "private/.git": b"gitdir: ../.git/modules/lsrules-private\n",
                    "git-marker": b"gitdir: ../.git/modules/lsrules-private\n",
                }, symlinks=symlinks, directories=directories,
                    git_reader=lambda *_: self.fail("Redirected metadata invoked Git."))
                self.assertEqual(status, 1)
                self.assertIn("private_submodule_boundary_verified", result["failures"])

    def test_git_metadata_redirects_fail_before_git_runs(self):
        for prefix in (".git", ".git/modules/lsrules-private"):
            for name, value in {
                "commondir": b"../elsewhere\n",
                "objects/info/alternates": b"../elsewhere\n",
                "objects/info/http-alternates": b"https://example.org/objects\n",
                "config": b"[include]\n\tpath = elsewhere\n",
                "config.worktree": b'[includeIf "onbranch:main"]\n\tpath = elsewhere\n',
            }.items():
                with self.subTest(prefix=prefix, name=name):
                    status, result = self.package_results({
                        ".gitmodules": check.PRIVATE_SUBMODULE_CONFIG.encode(),
                        "private/.git": b"gitdir: ../.git/modules/lsrules-private\n",
                        f"{prefix}/{name}": value,
                    }, directories=(".git/modules/lsrules-private",),
                        git_reader=lambda *_: self.fail("Redirected metadata invoked Git."))
                    self.assertEqual(status, 1)
                    self.assertIn("private_submodule_boundary_verified", result["failures"])

    def test_public_links_cannot_probe_private_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "README.md"
            for target in ("private/notes.md", "docs/../private/notes.md", "private%2Fnotes.md", "PRIVATE/notes.md", "private/child/../../README.md"):
                document.write_text(f"[Private]({target})\n")
                with self.subTest(target=target), patch.object(
                        Path, "resolve", side_effect=AssertionError("Private metadata was resolved.")), patch.object(
                        Path, "exists", side_effect=AssertionError("Private metadata was inspected.")):
                    self.assertFalse(check.local_references_valid(document, root))

    def test_git_evidence_commands_cannot_inherit_redirects_or_run_hooks(self):
        inherited = {"GIT_DIR": "elsewhere", "GIT_WORK_TREE": "elsewhere", "GIT_INDEX_FILE": "elsewhere", "PATH": "synthetic"}
        with patch.dict(os.environ, inherited, clear=True), patch.object(
                check.subprocess, "run", return_value=SimpleNamespace(stdout="result\n")) as run:
            self.assertEqual(check.read_only_git(Path("."), ["rev-parse", "--show-toplevel"]), "result\n")
            arguments = run.call_args.args[0]
            environment = run.call_args.kwargs["env"]
            self.assertNotIn("GIT_DIR", environment)
            self.assertNotIn("GIT_WORK_TREE", environment)
            self.assertNotIn("GIT_INDEX_FILE", environment)
            self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
            self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
            self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
            self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
            self.assertIn("protocol.allow=never", arguments)
            self.assertIn("core.fsmonitor=false", arguments)
            self.assertFalse(any("hooksPath" in argument for argument in arguments))
            run.reset_mock()
            self.assertIsNone(check.read_only_git(Path("."), ["commit"]))
            run.assert_not_called()

    def test_non_utf8_package_file_is_not_silently_ignored(self):
        with self.assertRaises(UnicodeDecodeError):
            self.package_results({"unexpected.bin": b"\x8b\x00"})

    def test_exact_document_provenance_passes_without_ignoring_its_directory(self):
        _, files = provenance_fixture()
        status, result = self.package_results(files)
        self.assertEqual(status, 0)
        self.assertEqual(result["failures"], [])

    def test_provenance_accepts_a_public_handle_reviewer(self):
        record, files = provenance_fixture()
        files[record] = files[record].replace(b"Example Reviewer <reviewer@example.org>", b"N4M3Z")
        status, result = self.package_results(files)
        self.assertEqual(status, 0)
        self.assertEqual(result["failures"], [])

    def test_changed_or_missing_document_bytes_never_exempt_a_digest(self):
        record, original = provenance_fixture()
        for name in original.keys() - {record}:
            for operation in ("change", "remove"):
                with self.subTest(name=name, operation=operation):
                    files = original.copy()
                    if operation == "change":
                        files[name] += b"Altered bytes.\n"
                    else:
                        del files[name]
                    status, result = self.package_results(files)
                    self.assertEqual(status, 1)
                    self.assertIn("document_provenance_bytes_verified", result["failures"])
                    self.assertIn("no_executable_fingerprints", result["failures"])

    def test_verified_digest_elsewhere_still_fails(self):
        record, original = provenance_fixture()
        digest = check.DOCUMENT_PROVENANCE.fullmatch(original[record].decode())["subject_digest"]
        for name in ("README.md", ".agents/notes.md", "docs/decisions/.provenance/notes.md"):
            with self.subTest(name=name):
                status, result = self.package_results({**original, name: digest.encode()})
                self.assertEqual(status, 1)
                self.assertIn("no_executable_fingerprints", result["failures"])
                self.assertNotIn("document_provenance_bytes_verified", result["failures"])

    def test_other_provenance_fields_do_not_exempt_digest_values(self):
        record, files = provenance_fixture()
        value = "e" * 64
        files[record] = files[record].replace(b"Example Reviewer <reviewer@example.org>", value.encode())
        status, result = self.package_results(files)
        self.assertEqual(status, 1)
        self.assertIn("no_executable_fingerprints", result["failures"])

    def test_malformed_or_extended_provenance_is_rejected(self):
        record, original = provenance_fixture()
        text = original[record].decode()
        cases = {
            "duplicate key": text.replace("  subject:\n", "  subject:\n  subject:\n"),
            "extra field": text + "extra: data\n",
            "extra document": text + "---\nextra: data\n",
            "anchor": text.replace("  subject:", "  subject: &subject"),
            "alias": text.replace("    digest:", "    digest: *subject", 1),
            "duplicate block": text + text[text.index("        - block:"):],
            "other replacement document": text.replace("Synthetic Decision.md:1", "Other Decision.md:1"),
            "escaped subject": text.replace("docs/decisions/LSR-", "docs/decisions/../LSR-", 1),
            "URL mismatch": text.replace("        uri: https://github.com/example/", "        uri: https://github.com/other/"),
            "comment": text.replace("Example Reviewer", "Example # Reviewer"),
            "mapping scalar": text.replace("Example Reviewer", "Example: Reviewer"),
            "path mismatch": text.replace("          path: replacements/", "          path: replacements/" + "e"),
            "invalid date": text.replace("2026-09-20T22:21:20.936339+00:00", "2026-99-20T22:21:20+00:00"),
            "reversed dates": text.replace("2026-09-20T22:21:20.936339+00:00", "2026-09-21T22:21:20+00:00"),
            "NUL in reviewer": text.replace("Example Reviewer", "Example\0Reviewer"),
            "control character": text.replace("Example Reviewer", "Example\x1bReviewer"),
            "YAML line separator": text.replace("Example Reviewer", "Example\u2028Reviewer"),
        }
        for indicator in "@%`]},":
            cases[f"forbidden scalar indicator {indicator}"] = text.replace("Example Reviewer", indicator + "Example")
        cases["boolean reviewer"] = text.replace("Example Reviewer <reviewer@example.org>", "true")
        for name, edited in cases.items():
            with self.subTest(name=name):
                status, result = self.package_results({**original, record: edited.encode()})
                self.assertEqual(status, 1)
                self.assertIn("document_provenance_bytes_verified", result["failures"])
                self.assertIn("no_executable_fingerprints", result["failures"])

    def test_provenance_cannot_move_to_an_unrelated_record_name(self):
        record, files = provenance_fixture()
        files[record.replace("LSR-0002", "LSR-0003")] = files.pop(record)
        status, result = self.package_results(files)
        self.assertEqual(status, 1)
        self.assertIn("document_provenance_bytes_verified", result["failures"])

    def test_provenance_and_referenced_documents_keep_all_privacy_checks(self):
        record, files = provenance_fixture()
        value = "/" + "Users/" + "example/config"
        files[record] = files[record].replace(b"Example Reviewer", value.encode())
        status, result = self.package_results(files)
        self.assertEqual(status, 1)
        self.assertIn("no_private_user_paths", result["failures"])
        files["docs/decisions/.provenance/.hidden-note"] = ("e" * 64).encode()
        status, result = self.package_results(files)
        self.assertIn("no_executable_fingerprints", result["failures"])

    def test_document_references_reject_symlink_files_and_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real"
            real.mkdir()
            document = real / "document.md"
            document.write_bytes(b"# A document\n")
            digest = hashlib.sha256(document.read_bytes()).hexdigest()
            file_link = root / "link.md"
            file_link.symlink_to(document)
            directory_link = root / "linked-directory"
            directory_link.symlink_to(real, target_is_directory=True)
            self.assertTrue(check.document_bytes_match(document, root, digest))
            self.assertFalse(check.document_bytes_match(file_link, root, digest))
            self.assertFalse(check.document_bytes_match(directory_link / document.name, root, digest))

    def test_referenced_documents_are_not_removed_from_privacy_scans(self):
        record, original = provenance_fixture()
        values = {
            "no_private_user_paths": "/" + "Users/" + "example/config",
            "no_literal_ip_addresses": ".".join(("192", "0", "2", "7")),
            "no_executable_fingerprints": "e" * 64,
        }
        for name in original.keys() - {record}:
            for failure, value in values.items():
                with self.subTest(name=name, failure=failure):
                    files = original.copy()
                    before = hashlib.sha256(files[name]).hexdigest()
                    contents = files.pop(name) + value.encode() + b"\n"
                    after = hashlib.sha256(contents).hexdigest()
                    files[name.replace(before, after)] = contents
                    files[record] = files[record].replace(before.encode(), after.encode())
                    status, result = self.package_results(files)
                    self.assertEqual(status, 1)
                    self.assertIn(failure, result["failures"])
                    self.assertNotIn("document_provenance_bytes_verified", result["failures"])

    def test_provenance_record_itself_cannot_be_a_symlink(self):
        record, files = provenance_fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, contents in files.items():
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(contents)
            path = root / record
            target = path.with_suffix(".original")
            path.rename(target)
            path.symlink_to(target)
            valid, text = check.verified_provenance_text(path, files[record].decode(), root)
            self.assertFalse(valid)
            self.assertEqual(text, files[record].decode())

    def test_symlinked_package_directory_cannot_hide_provenance(self):
        _, original = provenance_fixture()
        files = {name.replace("docs/decisions/.provenance", ".git/hidden-provenance"): data
                 for name, data in original.items()}
        status, result = self.package_results(files, {
            "docs/decisions/.provenance": ".git/hidden-provenance",
        })
        self.assertEqual(status, 1)
        self.assertIn("no_package_symlinks", result["failures"])

    def test_symlinked_hidden_file_cannot_bypass_package_scans(self):
        status, result = self.package_results({".git/hidden-note": b"data"}, {
            ".agents/hidden-note": ".git/hidden-note",
        })
        self.assertEqual(status, 1)
        self.assertIn("no_package_symlinks", result["failures"])

    def test_symlinked_policy_files_are_rejected_before_any_content_read(self):
        for name in ("rules/work-domains.json", "profiles/policy.json",
                     "catalog/blocklists.json", "rules/global-focus-disabled.lsrules"):
            with self.subTest(name=name), patch.object(
                    Path, "read_text", side_effect=AssertionError("Content was read before symlink rejection.")):
                status, result = self.package_results({".git/hidden-note": b"data"}, {
                    name: ".git/hidden-note",
                })
                self.assertEqual(status, 1)
                self.assertEqual(result["failures"], ["no_package_symlinks"])



class ResourceChecks(unittest.TestCase):
    def setUp(self):
        self.root = check.ROOT
        self.skill = self.root / ".agents/skills/lsrules-audit/SKILL.md"
        self.source = self.skill.read_text()
        self.data, self.body = check.frontmatter(self.source)

    def resource_results_with_text(self, path, replacement):
        original = Path.read_text

        def read(candidate, *args, **kwargs):
            return replacement if candidate == path else original(candidate, *args, **kwargs)

        with patch.object(Path, "read_text", read):
            return dict(check.agent_checks(self.root))

    def test_current_agent_resources_pass(self):
        self.assertTrue(all(passed for _, passed in check.agent_checks(self.root)))

    def test_skill_name_cannot_disagree_with_directory(self):
        edited = self.source.replace("name: lsrules-audit", "name: unrelated-skill", 1)
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_canonical_frontmatter"])

    def test_skill_h1_cannot_disagree_with_name(self):
        self.assertFalse(check.skill_structure("lsrules-audit", self.body.replace("# lsrules-audit", "# unrelated-skill", 1)))

    def test_instructions_section_is_required(self):
        self.assertFalse(check.skill_structure("lsrules-audit", self.body.replace("## Instructions", "## Background", 1)))

    def test_section_order_matters(self):
        edited = self.body.replace("## Prerequisites", "## Temporary", 1)
        edited = edited.replace("## Constraints", "## Prerequisites", 1).replace("## Temporary", "## Constraints", 1)
        self.assertFalse(check.skill_structure("lsrules-audit", edited))

    def test_duplicate_frontmatter_keys_fail(self):
        with self.assertRaises(ValueError):
            check.frontmatter(self.source.replace("name: lsrules-audit", "name: lsrules-audit\nname: another", 1))

    def test_yaml_executable_tag_is_not_interpreted(self):
        with self.assertRaises(ValueError):
            check.scalar("!!python/object:example ignored")

    def test_multiline_frontmatter_is_outside_safe_subset(self):
        with self.assertRaises(ValueError):
            check.frontmatter("---\nname: safe\ndescription: |\n  hidden continuation\n---\n# safe\n")

    def test_unsafe_dynamic_context_fails(self):
        edited = self.source + "\n!`external-command`\n"
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_bounded_static_entrypoint"])

    def test_companion_cannot_escape_skill_tree(self):
        edited = self.source + "\n[Outside companion](../../../README.md)\n"
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_local_references"])

    def test_missing_companion_fails(self):
        edited = self.source + "\n[Missing companion](missing.md)\n"
        results = self.resource_results_with_text(self.skill, edited)
        self.assertFalse(results["lsrules-audit_local_references"])

    def test_daybreak_model_cannot_silently_change(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = path.read_text().replace(check.DAYBREAK_MODEL, "different-model")
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_daybreak_read_only"])

    def test_daybreak_sandbox_cannot_gain_writes(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = path.read_text().replace('sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"')
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_daybreak_read_only"])

    def test_adapter_cannot_add_an_unreviewed_capability(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = 'web_search = "live"\n' + path.read_text()
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_fields_allowlisted"])

    def test_native_adapter_must_reference_canonical_contract(self):
        path = self.root / ".codex/agents/daybreak-adversary.toml"
        edited = path.read_text().replace(check.DAYBREAK_CONTRACT, ".agents/agents/missing.md")
        results = self.resource_results_with_text(path, edited)
        self.assertFalse(results["codex_adapter_canonical_contract_reference"])

    def test_ai_overlap_is_not_substring_matching(self):
        cases = [
            ("chatgpt.com", "chatgpt.com", True),
            ("proton.me", "lumo.proton.me", True),
            ("auth.openai.com", "openai.com", True),
            ("CHATGPT.COM.", "chatgpt.com", True),
            ("x.com", "x.ai", False),
            ("notopenai.com", "openai.com", False),
            ("openai.com.evil.example", "openai.com", False),
        ]
        for left, right, expected in cases:
            with self.subTest(left=left, right=right):
                self.assertEqual(check.domains_overlap(left, right), expected)


if __name__ == "__main__":
    unittest.main()
