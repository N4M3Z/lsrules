# Identity choices

Use a vendor Code ID when the installed executable has a verified stable publisher identity.
A vendor identity can survive routine version and path changes.
A code hash identifies one build and can require another decision after an update.

Keep process and via conditions separate.
A signed parent condition does not establish the integrity of an unchecked helper.
A rule for a parent without a via condition can also cover its helpers.
See [native code identity](https://help.obdev.at/littlesnitch6/adv-code-identity) and [rule format](https://help.obdev.at/littlesnitch6/adv-lsrules-file-format).

For frequently updated unsigned tools, choose the trust policy explicitly.
A path rule without an identity check avoids daily hash prompts but trusts replacement code at that path.
Limit such a helper to a signed parent, required hosts, protocol, ports, and profile where practical.
Keep that exception visible in policy metadata.
Do not silently replace a checksum requirement with a signing requirement to suppress a mismatch.

A reviewed helper path exception can keep a checked signed parent and narrow destinations.
Select the current installed executable through the native picker before creating a rule.
Keep local executable paths and fingerprints outside this repository.
A connection test proves connectivity. It does not prove executable integrity.

Review existing scope separately from identity changes.
Changing a helper identity does not justify changing its ports, hosts, direction, or profile.
A domain rule for all protocols and ports must not be described as an HTTPS-only rule.
