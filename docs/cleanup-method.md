# Targeted cleanup method

This method keeps useful targeted rules and removes only verified clutter.
It describes a review procedure. It contains no application inventory or native restore data.

## Capture the starting state

Use an existing complete backup when it answers the review question.
Create a new backup before broad changes when the existing evidence is incomplete.
Keep backups, machine identities, addresses, and detailed comparisons outside the repository.
Record the exact source bytes and later GUI changes in private evidence.

## Review one application at a time

Separate enabled rules, disabled rules, and review annotations.
A disabled rule can preserve a useful future restriction. Its disabled state alone does not justify deletion.
An inactive profile does not make its rules disabled.

Compare process, helper, identity, owner, destination, protocol, port, direction, action, profile, and priority.
Preserve distinct helper paths and identity requirements even when their visible descriptions look similar.
Check competing deny rules and native precedence before declaring an allow rule redundant.
Keep the retained covering rule unchanged during a bounded deletion.

Check blocklist priority before restoring a disabled targeted allow.
A host or domain allow can override a normal-priority blocklist entry.
Compare the proposed destination against the active lists before applying the change.
An empty overlap result applies only to the inspected list versions.
See the [rule precedence reference](https://help.obdev.at/littlesnitch6/concepts-rules).

Prefer exact hosts and required ports when evidence establishes the needed destinations.
Do not replace a stale helper path with a broad permission for newer executables.
Confirm that a fixed executable path is obsolete before removing its rule.
Do not treat a stale last-seen path as proof that a signed identifier or wildcard matcher is obsolete.

## Preserve intentional exceptions

Keep approved development exceptions visible in private policy records.
Review identity changes separately from destination changes.
A current binary hash can match a saved requirement without proving who approved that requirement.

Do not narrow a compatibility exception from a single observed destination.
Browser media, calls, VPN peers, and signing services can require broader evidence.
Test the required workflow before removing its fallback allowance.

## Verify the result

Verify saved GUI state after each bounded change.
Compare the resulting complete model with the starting evidence and the exact approved edits.
Preserve duplicate counts and every matching field.
Separate time fields, usage counters, review annotations, and executable identity requirements.
Report any unexplained difference instead of silently treating it as harmless metadata.

Use exact parent and helper selectors for application counts.
A GUI text filter can also match connection descriptions from other applications.
An empty Unapproved view confirms review state. It does not establish that every retained permission is necessary.

The saved model proves configuration at capture time.
Runtime tests add separate evidence for browsing, calls, DHCP, VPN transitions, and required application access.
This package does not implement the proposed offline cleanup auditor.
