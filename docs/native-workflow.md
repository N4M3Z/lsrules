# Native workflow

Review existing rules before importing any list.
An Unapproved marker is a review annotation. It does not change connection matching.
Review new rules before marking them seen.
Preserve deliberate denies and user-created scopes when clearing reviewed annotations.
See [rule concepts](https://help.obdev.at/littlesnitch6/concepts-rules).

The portable focus example starts disabled and has global scope.
Review its disabled state in the native app after import.
For Work-only restrictions, create the rule manually from `rules/work-domains.json` inside Work.
Do not enable a global group as a substitute for a Work rule.
See [rule groups](https://help.obdev.at/littlesnitch6/concepts-rulegroups).

Use the current native catalog for blocklist subscriptions.
Keep new allow rules disabled in remote groups.
Check update success and required application behavior after changes.
See [remote groups](https://help.obdev.at/littlesnitch6/lsc-rulegroups).

## Native commands

Check the installed native CLI help before manually using a command.
The bundled CLI can export the model and activate profiles.
It has no dedicated command for additive individual-rule editing.
This package provides no installer or host-applying script.
See [native commands](https://help.obdev.at/littlesnitch6/cmd-overview).

Create a native snapshot only when needed and permitted.
Keep it in a private directory outside the repository.
Backups include machine configuration, identities, and network details.
A backup describes the state when saved. Later GUI edits need separate evidence.
See [backups](https://help.obdev.at/littlesnitch6/lsc-backup).

## Dynamic Tailscale peers

Tailscale direct peers can use changing addresses and remote UDP ports.
The default UDP port 41641 refers to the local source port.
See [Tailscale firewall guidance](https://tailscale.com/docs/reference/faq/firewall-ports).

An explicitly approved option trusts the verified Tailscale network extension for outgoing UDP to any remote address and port.
This option broadens trust. Keep it inside the selected profile and retain its verified vendor Code ID.
Do not apply this choice automatically or extend it to other processes or profiles.
After saved-state verification, remove narrower allowances only when action, owner, identity, direction, and profile are covered.
Review incoming rules and TCP rules separately. An outgoing UDP allowance does not replace them.
Test direct and relay connectivity after the change. Report GUI verification separately from runtime test results.
