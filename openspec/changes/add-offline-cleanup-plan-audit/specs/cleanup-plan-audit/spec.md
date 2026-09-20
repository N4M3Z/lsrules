## Purpose

Judge an explicit cleanup plan against exact snapshot evidence and preserve uncertainty when an offline proof is insufficient.

## ADDED Requirements

### Requirement: Versioned plan bound to evidence
The auditor SHALL accept only a supported versioned plan tied to one exact snapshot digest and a canonical plan-content digest.
Each proposed operation SHALL have a unique operation identifier.
Existing-rule operations SHALL reference their source rule index and complete content fingerprint; additions SHALL contain a complete proposed record.
The auditor SHALL refuse a stale reference, mismatched fingerprint, unsupported operation, or unsupported plan version before evaluating changes.

#### Scenario: Correct index with stale rule content
- **WHEN** a plan references an existing index but its content fingerprint differs from that rule
- **THEN** the auditor refuses the plan rather than selecting a similar rule or another duplicate occurrence

### Requirement: Distinct candidate classes
The auditor SHALL distinguish disabled allowance clutter, exact duplicates, provable coverage, and candidates that need more evidence.
A candidate label SHALL describe its evidence basis and SHALL not itself authorize deletion.
Endpoint churn, age, low use, an Unapproved annotation, or an inactive profile alone SHALL not establish obsolescence.

#### Scenario: Changing peer endpoint without coverage
- **WHEN** a plan deletes a used endpoint rule because its address changed and supplies no coverage or obsolescence evidence
- **THEN** the operation receives `needs-evidence` rather than a provable-coverage or obsolete-rule decision

### Requirement: Conservative same-scope comparison
A duplicate or coverage proof SHALL compare action, direction, owner, process, via, identity, profile, group, priority, and destination conditions.
It SHALL also compare protocol, ports, enabled state, and any other condition that can affect matching.
Any unclassified field on a subject, witness, or potential competitor SHALL produce `needs-evidence`; only explicitly nonsemantic metadata can be ignored.

#### Scenario: Same destination with a different parent
- **WHEN** two allowances share a destination but restrict different via processes or parent identities
- **THEN** the auditor does not treat the allowances as interchangeable based on their destination alone

### Requirement: Native precedence uncertainty blocks proof
A coverage proof SHALL account for relevant overlapping deny or ask rules and supported native precedence conditions.
It SHALL consider applicable all-profile rules and the affected profile without treating profiles as mutually inherited baselines.
If the supported analysis cannot establish preserved decisions, the operation SHALL receive `needs-evidence` with the unresolved condition.

#### Scenario: Narrow allowance overlaps a deny
- **WHEN** a proposed deletion leaves a broader allowance but an overlapping deny could change the winning native decision
- **THEN** the auditor withholds a coverage acceptance unless its supported precedence proof resolves that interaction

### Requirement: Evaluate the complete proposed deletion set
The auditor SHALL evaluate deletion dependencies against the complete plan, preserving rule occurrence counts.
A coverage witness SHALL be an enabled original rule occurrence that survives the complete plan unchanged.
Proposed additions or replacements SHALL not provide coverage witnesses for deletions.
An explicitly proven dependency failure SHALL reject the affected deletion; cyclic or unsupported dependencies SHALL not receive acceptance.

#### Scenario: Both duplicate occurrences are deleted
- **WHEN** two duplicate rules each cite the other as their only surviving coverage and the plan deletes both
- **THEN** the auditor rejects the dependent deletions instead of accepting two separate duplicate proofs

#### Scenario: Proposed replacement is the only witness
- **WHEN** a deletion cites a newly proposed or changed allowance as its only coverage witness
- **THEN** the auditor does not accept an equivalent-cleanup proof and reports the separate scope and native ordering evidence required

### Requirement: Management and lifetime conditions gate acceptance
The auditor SHALL consider source, group management, protection, mutability, and lifetime before accepting a duplicate or coverage deletion.
It SHALL not equate an editable rule with a protected subscription rule or a persistent rule with a temporary witness without proof.
Unresolved management effects or lifetime semantics SHALL produce `needs-evidence`.
Version 1 SHALL reject direct edits to rules known to be protected or externally managed.

#### Scenario: Equal selectors with different management
- **WHEN** an editable persistent rule appears equal to a protected group-managed rule with uncertain lifetime
- **THEN** the auditor returns `needs-evidence` rather than accepting deletion based only on the equal selectors

### Requirement: Preserve deliberate boundaries and required workflows
The auditor SHALL evaluate supplied protected-workflow inventory, including required ChatGPT access, before accepting an affected operation.
Removing or weakening a deny, required transport, parent identity, or protected workflow SHALL require explicit authorization for that exact change.
Missing workflow inventory or unresolved impact SHALL produce `needs-evidence`, not an assumption that the workflow is unnecessary.

#### Scenario: Cleanup removes a ChatGPT transport
- **WHEN** an operation removes a required ChatGPT transport without authorization that specifically covers its loss
- **THEN** the auditor rejects the unauthorized operation or returns `needs-evidence` when its impact cannot be established

### Requirement: Broader network policy requires scoped authorization
An operation that broadens remote, port, protocol, process, owner, profile, or identity trust SHALL carry attributed authorization evidence.
Authorization SHALL bind the snapshot digest, canonical plan digest, exact operation set, complete before-and-after scopes, and attributed decision source.
Its authenticity SHALL remain unverified documentary evidence; a matching bound documentary record SHALL not trigger the same record request again.
Results SHALL retain `authorization_authenticity: unverified` even when documentary binding passes.
Broader policy SHALL never be labeled equivalent cleanup; acceptance SHALL require separate scope and native application-order evidence.

#### Scenario: Documented Tailscale UDP consolidation
- **WHEN** a plan broadens Trusted outgoing UDP for the snapshot-recorded Tailscale Code ID and supplies a matching bound documentary record
- **THEN** the auditor evaluates that declared scope without authenticating consent, verifying the current binary, or extending the record to other profiles or processes

#### Scenario: Authorization reused after a plan edit
- **WHEN** a broader plan changes after its attached authorization was bound to the earlier plan digest
- **THEN** the auditor treats that authorization as mismatched and returns `needs-evidence` for the broadened operation

### Requirement: Identity exceptions remain bounded
An unchecked-helper exception SHALL retain a separately represented signed parent and its explicitly authorized connection constraints.
The auditor SHALL compare an identity edit separately from destination, direction, transport, and profile edits.
A helper exception SHALL not authorize removing unrelated CLI identities or treating a connection result as integrity proof.

#### Scenario: One helper exception expands to every CLI
- **WHEN** a plan cites authorization for one frequently updated helper but removes identity checks from unrelated CLI rules
- **THEN** the auditor rejects those unrelated changes as outside the supplied authorization scope

### Requirement: Deterministic operation verdicts
Each auditable operation SHALL receive `accept`, `reject`, or `needs-evidence`, plus stable reason codes and its proof or missing evidence.
Identical snapshot, plan, evidence, and auditor versions SHALL produce identical verdicts and ordering.
`accept` SHALL mean that the proposed operation satisfies this offline contract, not that native enforcement or host behavior was verified.

#### Scenario: Unsupported destination semantics
- **WHEN** a coverage decision depends on a selector outside the supported comparison rules
- **THEN** the auditor deterministically returns `needs-evidence` and names that unsupported comparison in the private report

### Requirement: Bounded analysis without partial acceptance
Version 1 SHALL limit each run to 1,000,000 candidate comparisons and stop when further analysis would exceed that budget.
An exhausted run SHALL report an analysis-limit error rather than a complete or accepted audit.

#### Scenario: Overlap analysis exceeds its budget
- **WHEN** a supported snapshot requires more comparisons than the declared run budget
- **THEN** the auditor reports the limit without accepting the unexamined plan or presenting partial decisions as complete

### Requirement: Offline planning remains separate from application
The auditor SHALL produce decisions without editing host rules, exporting snapshots, restoring models, activating profiles, or making network requests.
It SHALL not implement or claim a complete native enforcement emulator.
Runtime observations SHALL remain separate attributed evidence and SHALL not silently change the supplied snapshot or plan.

#### Scenario: Accepted plan requests automatic application
- **WHEN** a valid plan contains an instruction to apply accepted changes or probe a remote service
- **THEN** the auditor performs neither action and treats the instruction as data or refuses it as an unsupported plan operation
