# Publication procedure

Public target: `N4M3Z/lsrules`. The owner selected public visibility and EUPL-1.2 for the package.
This procedure defines the boundary for future publication changes.
Keep local preparation, commits, repository creation, and uploads as separate verified states.
Recheck the destination before an authorized creation or upload.

## Publication contents

Publish the reviewed portable policy, source catalog, procedures, validators, canonical agent resources, and scoped upstream notices.
Include hidden `.agents` and `.codex` files in the review.
The proposed cleanup auditor remains unimplemented and clearly labelled as a proposal.

Keep native backups, application inventories, machine cleanup history, addresses, executable fingerprints, and local verification reports outside the publication set.
The [cleanup method](docs/cleanup-method.md) retains reusable procedures without the machine record.
The complete machine record remains in separate private evidence.
Use the [private submodule](docs/private-companion.md) for separately reviewed personal policy and machine data.
The owner selected `N4M3Z/lsrules-private` at `private/` on 2026-10-17.
Public metadata exposes that repository URL and its selected commit. It must exclude every private payload file.
Approve each private upload separately from public publication.
An earlier bootstrap approval does not authorize later machine-data uploads.

## History boundary

The existing local history contains machine-specific author metadata.
Do not push that history as part of this publication.
Prepare a clean initial publication commit from the reviewed file snapshot after approval.
Preserve the original local repository and its history.
Do not use a mirror push, an all-ref push, or an automatic history rewrite.

Use the owner's public handle and public noreply address for the publication author identity.
The exact file manifest and validation record must match the snapshot used for the new commit.
Any later file change requires renewed validation and an updated manifest.

The original source checkout uses Jujutsu, which does not support submodule edits.
The publication checkout uses Git and holds the private submodule.
Preserve the original source checkout and its metadata.
A private submodule change alone does not authorize a public parent upload.

## Checks before publication

Run these local checks with Python 3.11 or later:

```sh
python3 -B scripts/check.py
python3 -B scripts/test_check.py
```

Inspect the final file snapshot for credentials, native captures, generated caches, symlinks, and machine-specific data.
Verify the exact submodule declaration and selected commit separately from public file contents.
Never traverse or include the private submodule when building the public archive.
Run a local secret scan on that exact snapshot.
Review policy and privacy claims independently under the canonical adversary contract.
Record the actual review model when runtime evidence supplies it.
An unavailable Daybreak model must remain an explicit review limitation.

## License and source scope

The package uses [EUPL-1.2](LICENSE). Adopted material retains the [upstream notices](THIRD_PARTY.md).
The package contains no third-party blocklist contents.
The [source review](catalog/review-2026-10-17.md) records current access and license limits.
The owner selected EUPL-1.2 for the original files on 2026-10-17.

A private repository does not support an anonymous raw subscription endpoint.
Do not add credentials to a subscription URL or committed configuration.

## Required owner approval

The user must approve the exact public file snapshot before the public initial commit, repository creation, or upload.
Approval must identify the destination, visibility, initial publication history, and operation.
Local preparation does not authorize publication.
After an authorized upload, verify the remote tree and report the resulting commit and repository separately.
