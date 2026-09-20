## Context

See [proposal.md](proposal.md) for the problem and proposed capabilities.
The current package has an offline structure checker, policy references, three skills, and a Daybreak adapter.
It has no native snapshot parser, cleanup-plan contract, or rule-coverage engine.

The first implementation will use explicitly supplied evidence and produce a review result.
It will never discover live configuration, create another backup, or drive Little Snitch.

## Goals / Non-Goals

**Goals:**

- Make each cleanup decision reproducible from a snapshot, plan, and explicit policy constraints.
- Justify a small supported subset of changes against bound evidence and expose unsupported comparisons.
- Preserve duplicate instances, process pairs, profile boundaries, and competing rules during comparison.
- Produce useful private detail without leaking that detail into normal terminal output or public artifacts.

**Non-Goals:**

- A complete emulator of Little Snitch precedence or current network state.
- A rule installer, native backup exporter, GUI controller, or live network monitor.
- Automatic approval of broader permissions because an agent recommends them.
- Automatic remote model invocation, blocklist downloads, or publication.

## Decisions

### 1. Use a bounded native JSON adapter

Add standard-library Python modules behind a small command entrypoint.
Keep the existing package checker separate so policy checks remain useful without a snapshot.

The first adapter accepts the plaintext JSON model shape represented by reviewed Little Snitch 6 evidence.
Support is determined by recognized structure and fields, not by the filename extension alone.
Reject archives, encoded objects, duplicate JSON keys, nonfinite numbers, and unsupported top-level structures.
Limit input to 32 MiB, 100,000 rules, and 64 nesting levels.
Apply equivalent bounds to plan and scope documents.
Limit candidate comparisons to one million per run.
Exhaustion returns a fixed analysis-limit error without a complete or accepted result.

Use explicit adapters for documented defaults and version-specific fields.
Preserve unknown fields as unresolved evidence. Do not map an unknown selector to Any Server or an absent profile to global scope.
Any unclassified field on a subject, witness, or potentially competing rule prevents an affected decision from receiving `accept`.
Only metadata explicitly classified as non-semantic can be excluded from comparison.
Keep every raw field and its location in private evidence.

Alternative: a universal normalizer could hide native distinctions and silently widen matches.
A bounded adapter makes unsupported evidence visible.

### 2. Bind rule instances and edits to immutable evidence

Define versioned JSON contracts for normalized rule evidence, a cleanup plan, scope constraints, and audit results.
Bind each plan to the digest of the exact snapshot bytes.
Reference a rule by its original array position and a digest of its canonical raw record.
Do not use a process name, GUI search count, or generated identifier alone.
Keep identical duplicate records as separate instances.

Use a versioned canonicalization named `python-json-v1` for record and plan fingerprints.
Serialize parsed JSON as UTF-8 with sorted object keys, compact separators, preserved array order, and non-ASCII characters unescaped.
Use the supported Python JSON number representation and forbid nonfinite values. Do not claim compatibility with another canonical JSON standard.
Hash a version-tagged envelope so future canonicalization changes cannot silently reuse existing references.
The plan digest covers its payload, including operation identifiers and order, but excludes the digest field and attached review records.
Authorization records bind that digest from a separate scope document, avoiding a self-referential hash.

Supported plan actions are remove, annotate, add, and replace.
Existing-rule actions require source references. Additions require a complete proposed record and a unique operation identifier, without a source index.
Replacement contains the complete expected before record and complete proposed after record.
Annotation operations can change only the approved marker and notes allowed by the adapter.
Candidate discovery is advisory. It never becomes permission to apply a plan.

Construct the proposed final model in memory before assessing coverage.
This prevents two removals from each claiming that the other rule remains as their replacement.
In v1, a coverage witness must also be an unchanged original rule instance.
An addition or replacement cannot justify a deletion because the auditor does not prove safe native application order.
Plans that rely on that ordering receive `needs-evidence` for the dependent deletion.

Alternative: textual diffs and live row numbers cannot reliably identify duplicate instances or stale inputs.

### 3. Keep the proof engine deliberately conservative

Compare action, direction, process, via process, identity conditions, owner, destination selector, protocol, ports, profile, priority, and enabled state.
Keep path, Code ID, signing chain, hash requirement, parent condition, and unchecked-path state as distinct typed identity fields.
Compare lifetime, group membership and type, group state, source, protection, and mutability as management semantics.
Unknown management semantics produce `needs-evidence`.
Direct edits to protected or externally managed rules receive `reject` because v1 has no supported mutation operation for them.
Keep review annotations separate from traffic semantics.
Check profile scope for every potentially active profile. An inactive profile does not make its enabled rules disposable.

The initial engine can prove disabled clutter, exact semantic duplicates, and simple containment in a retained rule.
Containment is eligible only when action, process pair, identity, owner, profile, protocol, direction, and priority agree.
The retained rule must remain enabled and unchanged in the proposed final model.
Destination and port containment must belong to a supported comparison family.
Known exact selectors can compare for equality. Any Server can cover known supported remote selectors.
Address and port ranges can use explicit containment without DNS resolution.
Do not infer host-to-address or cross-type domain equivalence.

Before accepting coverage, inspect other rules that can compete with the removed rule or replacement.
An overlapping action, ask, priority, profile, lifetime, or group-state difference produces `needs-evidence` unless incompatibility is proven.
An unclassified field in a potential competitor also produces `needs-evidence`.
A proven change outside explicit scope produces `reject`.
Allow-versus-deny equivalence is never a redundancy proof.

This restriction matters because a specific allow can override a deny that a broader replacement would not override.
The engine does not infer equivalence from two Allow labels.

Alternative: fully reproducing native precedence would increase the initial proof and compatibility burden.
The first version accepts fewer automatic conclusions and explains each unresolved comparison.

### 4. Represent authorization as scope evidence

The scope document names allowed operations, affected rule instances, permitted field changes, and protected workflow selectors.
It binds the exact snapshot digest, canonical plan digest, complete operation set, and before/after field scopes.
Changing any bound plan field invalidates that authorization record.
Required ChatGPT access is an explicit protected workflow in the audit procedure.
Missing workflow evidence prevents a report from claiming that workflow preservation was verified.

A broader process permission requires an authorization record tied to the exact before and after scope.
The auditor can verify this binding. It cannot authenticate a person's consent from a self-authored JSON assertion.
Reports label that distinction and require the operator to confirm the record against the actual user request.
Use the fixed result flag `authorization_authenticity: unverified` even when documentary binding passes.
The auditor never executes a change, even when it returns `accept`.

Changing an unsigned helper's identity policy is separate from changing its destinations or profile.
Changing remote peer ports is separate from allowing all UDP traffic for a browser or VPN process.
Service documentation can explain a transport requirement. Historical observations cannot establish continued user need.

### 5. Separate safe output from private evidence

The default command output is a versioned JSON summary of aggregate counts, fixed reason codes, and evidence-status flags.
It excludes paths, source digests, rule identifiers, addresses, domains, profile names, notes, and raw parser errors.
It never copies unrecognized input fields into output.
Apply the same allowlist to stderr, usage errors, parser errors, and exceptions.
Do not echo paths, raw values, field locations, or exception messages in either stream.
Accept input files only through explicit path arguments. Do not accept native evidence through stdin in v1.

Detailed reports and generated candidate plans require explicit private output paths outside the repository.
Create each output exclusively with owner-only permissions.
Reject existing destinations, symlink traversal, and paths that resolve inside the repository.
Refuse writes when safe creation cannot be established. Do not fall back to detailed stdout.
Input and error handling must not create caches or temporary copies of native evidence.

Public test fixtures use documented synthetic data assembled in memory.
No private snapshot, observed hostname, executable fingerprint, or machine address is copied into a fixture.
Keep the existing repository leak checks. Add targeted tests of public-summary serialization.

Alternative: redacting a detailed report can miss free text, nested fields, and malformed-input diagnostics.
An allowlisted public serializer provides a smaller disclosure surface.

### 6. Keep deterministic checks separate from agent judgment

The CLI does not start Daybreak or any other model.
The audit skill can request an independent review of the plan and synthetic decision cases within the user's authorized review scope.
Record the reviewed snapshot, plan, result digests, findings, reviewer role, and observed runtime model when available in the private review record.
An adapter's configured model is not runtime evidence.

Agent review can challenge missing evidence or an invalid assumption.
It cannot turn `reject` or `needs-evidence` into `accept` by changing a label.
Revise the inputs or implementation and run the deterministic audit again.
The public summary records only whether an independent review is absent, incomplete, or complete with unresolved findings.
An optional private review record must bind the snapshot, plan, and deterministic result digests.
It is reported separately and cannot alter a deterministic decision.

### 7. Define a small command surface and stable exit behavior

Use `python3 -B scripts/audit.py candidates --snapshot SNAPSHOT --private-output PLAN` for candidate plans.
Use `python3 -B scripts/audit.py review --snapshot SNAPSHOT --plan PLAN --scope SCOPE` for review.
An optional `--private-output REPORT` writes the detailed review result under the private-output rules.
An optional `--review-evidence RECORD` attaches a bound independent-review record without changing the deterministic verdict.
These are proposed interfaces. They do not exist in the current package.

The plan contract contains `schema_version`, `snapshot_digest`, `canonicalization`, `operations`, and its separately computed `plan_digest`.
Each operation has an identifier, action, source reference when required, proposed record when required, and evidence references.
The scope contract contains bound digests, allowed operation identifiers, complete permitted field deltas, protected workflows, and authorization references.
The result contract separates deterministic decisions, aggregate output, private provenance, and independent review metadata.
The implementation must document required keys and reject unknown control keys before interpreting these contracts.

Exit 0 means a valid candidate run or a review with all decisions accepted.
Exit 1 means a valid review contains rejected or unresolved decisions.
Exit 2 means invalid input, unsupported format, unsafe output, or another execution error.
All results state snapshot-only evidence status. None claims current native enforcement.

## Risks / Trade-offs

- Incomplete native field knowledge can hide behavior. Reject unsupported shapes and retain unknown matcher status.
- Conservative precedence checks can produce many unresolved cases. Report the competing rule and the missing proof.
- Large overlap sets can exhaust comparison work. Enforce the analysis budget and report no complete result after exhaustion.
- Old snapshots can be accurate but stale. Bind results to their source and list later observations separately.
- Low use counts can describe rare essential media traffic. Require service and workflow evidence before proposing removal for obsolescence.
- A forged authorization record can look complete. Report its documentary status and require operator verification.
- Private file paths can cross symlinks or race with another process. Use secure exclusive creation and refuse unsafe paths.
- Agent findings can be wrong. Require reproducible counterexamples and primary evidence before changing a decision.

## Migration Plan

Add the audit capability beside the existing package checker and keep current policy files unchanged.
Use generated synthetic cases for development and CI.
Any later test with a private snapshot requires an explicit path and private report destination.
Update the audit skill only after the command behavior and adversarial tests pass.

Rollback removes the new audit entrypoint and its skill references. There is no host-state rollback because the auditor applies nothing.
Archive this change only after implementation, scenario validation, and independent review are complete.

## Review Evidence

An independent Daybreak review of the existing package supplied the initial acceptance risks for this proposal.
It identified missing native parsing and coverage proofs, distinct evidence types, profile leakage, privacy, and changing media endpoints.
This review does not establish that the proposed implementation works.
The second Daybreak review found gaps in witness provenance, management semantics, unknown fields, scope binding, and failure-output privacy.
The design now requires unchanged original witnesses, explicit management gates, plan-bound scope records, and safe stdout and stderr.
The specs and tasks must include the corresponding negative cases before the proposal is ready for implementation review.
