# Publication validation repair record

The existing subject digest and four replacement digests match their local document bytes.
The upstream digest matches the historical CORE-0019 document from the local deck repository.
The exact source comes from commit `1e016dbe972ce07d5fce9b44fc2928680b5c6d2b`.
Its source path is `docs/decisions/CORE-0019 Spec-Driven Change Lifecycle.md`.
The recovered document has 2,845 bytes. Its content remains unchanged.

The validator supports the existing adoption emitter structure and rejects unsupported syntax.
It masks exact verified digest occurrences only during the fingerprint check.
It scans every record and referenced document for other private content.
It does not establish the authorship or authenticity of the source.

The final regression run passed all 47 tests. The package check passed all 47 checks.
The change specification passed validation without findings.
The checker and test patch passed the whitespace check.

An independent static review found malformed control characters, invalid scalar indicators, and omitted symlink directories.
The repair rejects those cases and adds regression coverage.
The final ordering review moved symlink rejection before every package content read, including required policy and catalog files.
The new regression case fails if any text read occurs before symlink rejection.
The privacy scan detects IPv6 literals with standard-library validation and no network activity.
Its synthetic cases cover bracketed URLs, compressed and mapped addresses, and raw or URL-encoded zone suffixes.
The tests also cover address literals followed by sentence punctuation, including a trailing colon.
Ordinary colon prose, timestamps, and version strings remain valid.
The package permits only the exact `lsrules-private` declaration at the root `private` path.
Public traversal never descends into the private boundary.
An absent or empty declared checkout needs no Git command.
A populated checkout requires the expected Git worktree, a commit HEAD, and the matching staged gitlink.
The check rejects unexpected public repository metadata and symlinked private roots or Git metadata paths.
The check verifies both worktree roots and rejects Git metadata redirects before it invokes Git.
Public document references cannot probe the private boundary or its payload.
The initialized cases use mocked read-only Git evidence and do not establish a successful live submodule link.
No fixture repository, fixture commit, signing exception, or hook bypass forms part of these tests.
The public handle reviewer form passes without changing any subject, source, or replacement digest.

Final publication review lives in separate private release evidence and must reference the exact candidate manifest.

This change remains local and is not archived or accepted.
