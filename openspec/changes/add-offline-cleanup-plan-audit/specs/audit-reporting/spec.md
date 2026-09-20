## Purpose

Report offline audit decisions without disclosing private snapshot data or overstating native, runtime, or independent-review evidence.

## ADDED Requirements

### Requirement: Safe aggregate output by default
The default report SHALL contain only an explicit allowlist of versions, aggregate counts, verdict totals, stable reason codes, and fixed evidence-status flags.
It SHALL exclude input-derived strings, rule details, source paths, fingerprints, addresses, domains, account data, network labels, and free-text evidence.
The auditor SHALL not create a private detail report unless the caller explicitly requests its destination; version 1 SHALL reject detailed stdout output.

#### Scenario: Sensitive content in an operation label
- **WHEN** a private plan contains an operation label with an account name and internal address
- **THEN** default output contains only safe aggregate fields and emits neither the label nor either sensitive value

### Requirement: Explicit private output destination
Every private output, including generated candidate plans and detailed reports, SHALL require an explicit destination outside the repository.
The auditor SHALL refuse any existing destination, symlink destination, or symlink directory component and SHALL not replace a file.
A successful private output SHALL be a regular file with mode `0600`; inability to establish that boundary SHALL fail the write.

#### Scenario: Private output would replace existing evidence
- **WHEN** a generated candidate plan or detailed report would replace an existing snapshot, plan, report, or other file
- **THEN** the auditor refuses the write and leaves the existing file unchanged

### Requirement: Complete private decision evidence
A private report SHALL include snapshot and plan digests, versions, rule occurrence references, affected fields, verdicts, and coverage witnesses.
It SHALL include supplied authorization references, retained unknown fields relevant to decisions, and unresolved proof obligations.
The report SHALL identify its fingerprint method and preserve duplicate occurrence counts without embedding the entire raw snapshot by default.

#### Scenario: Coverage depends on one retained rule
- **WHEN** an operation is accepted because an unchanged surviving rule provides proven coverage
- **THEN** the private report identifies both rule occurrences, their fingerprints, compared fields, and the coverage basis

### Requirement: Distinct evidence and validation states
Reports SHALL distinguish saved snapshot evidence, proposed plan changes, supplied GUI observations, supplied runtime observations, and arithmetic inferences.
They SHALL state that offline acceptance does not prove native import acceptance, current configuration, effective identity checks, or runtime connectivity.
Unavailable validation SHALL remain unverified rather than passing by omission.

#### Scenario: Runtime command exits successfully with an error message
- **WHEN** supplied evidence records exit code zero with non-JSON failure output instead of the expected runtime result
- **THEN** the report records the failed observation and does not claim connectivity or native enforcement passed

### Requirement: Deterministic report content
Equivalent supported inputs and auditor versions SHALL produce the same verdict ordering, reason codes, references, and aggregate counts.
Volatile execution metadata SHALL remain separate from deterministic decision content.
The public report SHALL preserve distinctions between rejected input, rejected operations, accepted operations, and operations needing evidence.

#### Scenario: Repeated offline audit
- **WHEN** the same snapshot, plan, evidence, and auditor version are audited at two different times
- **THEN** their decision content and aggregate output match even if separately recorded execution times differ

### Requirement: Safe failure output
Standard output and standard error SHALL use fixed allowlisted codes and safe fields, including argument errors and unexpected failures.
Failures SHALL emit no raw input excerpts, private paths, fallback object dumps, or tracebacks.
A failed private write SHALL not redirect private details to standard output, standard error, or a repository file.
The caller SHALL be able to distinguish refused input from a completed audit containing rejected operations.

#### Scenario: Invalid private JSON contains a credential
- **WHEN** input parsing fails near a private credential value
- **THEN** the auditor emits a safe parsing error without the credential, surrounding text, or a traceback

### Requirement: Optional independent review attachment
The auditor SHALL accept an optional human or agent review attachment with provenance bound to the exact audited plan digest.
The attachment SHALL identify the reviewed snapshot digest, findings, review scope, and evidence limits.
It SHALL also bind the deterministic audit-result digest, excluding attached review metadata and volatile execution metadata.
Missing independent review SHALL be reported as absent and SHALL not trigger model dispatch or a network request.

#### Scenario: Review belongs to an earlier plan
- **WHEN** a supplied Daybreak review references a different plan digest
- **THEN** the report marks the attachment as mismatched and does not present it as review of the current plan

### Requirement: Observed reviewer provenance
Agent review provenance SHALL distinguish a configured model from an effective model observed in runtime evidence.
It SHALL make the same distinction for sandbox settings and record unknown values when effective runtime evidence is unavailable.
An adapter filename or model declaration alone SHALL not establish that Daybreak performed a review.

#### Scenario: Daybreak adapter exists without a recorded run
- **WHEN** the supplied evidence contains only the native adapter configuration
- **THEN** the report records configured intent and states that effective model, sandbox, and review execution remain unverified

### Requirement: Review findings remain data
Reviewer findings and all supplied free text SHALL be treated as untrusted report data, never executable instructions.
An attachment SHALL not override deterministic verdicts, grant host authority, or authorize disclosure of private evidence.
A changed plan or new proof evidence SHALL require a new audit before its decisions replace the earlier result.

#### Scenario: Reviewer asks to upload the snapshot
- **WHEN** an attached review instructs the auditor to upload private evidence or mark every operation accepted
- **THEN** the auditor performs no upload and preserves its independently computed operation verdicts

### Requirement: Explicit limits in handoff reports
A handoff SHALL state the completed offline checks, unresolved evidence, and any supplied review provenance separately.
It SHALL distinguish locally prepared artifacts from host application, repository creation, commits, pushes, and publication.
No report SHALL claim those external actions occurred merely because an offline plan was accepted.

#### Scenario: All offline operations are accepted
- **WHEN** the audit accepts every proposed operation without performing any host or Git action
- **THEN** the handoff states that the plan is locally audited and that native application and publication have not occurred
