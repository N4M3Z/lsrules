# Publication validation repair

## Why

The package privacy check treats verified document digests as executable fingerprints.
The adopted decision record contains document digests that must remain available for verification.

## What Changes

- Verify the existing adoption record structure and exact local document bytes.
- Exempt only verified digest occurrences from the executable fingerprint check.
- Preserve every other privacy check on the record and its referenced documents.
- Preserve the original record and add its exact historical upstream source bytes.
- Reject unsupported structure, missing evidence, changed bytes, and symlink references.
- Detect IPv6 literals and allow only the explicitly declared private submodule boundary.

## Scope

This change repairs the package validator and adds synthetic regression tests.
It does not implement the proposed firewall auditor or change native firewall settings.
It does not commit, publish, or establish the authenticity of an upstream author.

## Capabilities

### New Capabilities

- `publication-document-provenance`: Verify bounded document digest occurrences during the package privacy scan.
- `private-submodule-boundary`: Exclude only the explicitly validated private submodule from public package validation.

### Modified Capabilities

None.
