# Publishing

Publish reusable policy and guides to `N4M3Z/lsrules`.
Publish approved personal policy only to the private `N4M3Z/lsrules-private` repository.
Native backups and detailed machine evidence remain local.
The public repository exposes the private repository URL and commit, but none of its contents.

Before an approved push:

1. Run `make validate` and inspect the exact diff for personal data and credentials.
2. Run the existing secret scan and hooks. A secret scan cannot detect all personal information.
3. For a private update, verify private visibility and push the approved child commit first.
4. Record that commit as the public submodule pointer. Exclude private payload files from public archives.
5. Verify the remote commit after each push.

Use an identity in `authors.yaml` and preserve signing.
Approval must cover the exact changes, destination, and operation.
Keep the original source checkout and its history separate from this publication checkout.
Do not push unrelated history, all refs, or a repository mirror.

The public package uses [EUPL-1.2](LICENSE). Preserve the [third-party notices](THIRD_PARTY.md).
The license does not cover external blocklist contents or private companion data.
Private GitHub files are not anonymous subscription endpoints. Never put credentials in a rule-group URL.
