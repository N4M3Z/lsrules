## Purpose

Preserve exact private snapshot evidence for an offline cleanup audit without implying current host state or native enforcement.

## ADDED Requirements

### Requirement: Explicit supported snapshot input
The auditor SHALL read only an explicitly supplied private plaintext JSON snapshot file outside the repository; version 1 SHALL reject stdin data.
It SHALL accept only the declared supported Little Snitch 6 object shape, including an ordered `rules` array of objects.
It SHALL refuse unsupported formats and invalid shapes without exporting a snapshot, unpacking an archive, or contacting an application.

#### Scenario: Archive supplied as a snapshot
- **WHEN** the supplied file is an archive rather than supported plaintext native JSON
- **THEN** the auditor refuses the input with a stable format error and performs no extraction or host operation

### Requirement: Bounded complete parsing
The auditor SHALL declare finite input-size and nesting limits and refuse inputs that exceed them.
It SHALL refuse ambiguous JSON, including duplicate object keys and non-finite numeric values.
It SHALL not truncate rules or continue with a partially parsed snapshot.

#### Scenario: Conflicting duplicate keys
- **WHEN** one rule object contains two values for its action key
- **THEN** the auditor refuses the snapshot instead of choosing either value

### Requirement: Exact evidence identity
The auditor SHALL compute a SHA256 digest over the exact snapshot bytes used for analysis.
It SHALL record the supplied source, digest, observation time, and parsing method as private provenance.
It SHALL distinguish an observed file time from a native save time and leave unavailable native version or time metadata unknown.

#### Scenario: Snapshot changes after an earlier audit
- **WHEN** the newly supplied bytes differ from the bytes referenced by a cleanup plan
- **THEN** the auditor reports a digest mismatch and does not audit that plan against the changed snapshot

### Requirement: Stable rule occurrence references
The auditor SHALL reference each rule by its zero-based source index and a deterministic content fingerprint.
The fingerprint method SHALL be versioned and cover the complete rule object, including unknown fields.
Equal rule objects at different indices SHALL remain distinct occurrences in every inventory and comparison.

#### Scenario: Two identical rule occurrences
- **WHEN** the snapshot contains two identical rule objects at different indices
- **THEN** the inventory retains both occurrences with their distinct indices and matching content fingerprints

### Requirement: Lossless evidence inventory
The auditor SHALL retain original rule fields and supporting snapshot objects without dropping unfamiliar fields.
It SHALL keep code requirements, profiles, groups, defaults, and other source metadata available to the private audit.
An unclassified field on a subject, witness, or potential competitor SHALL block coverage proof; only explicitly nonsemantic metadata can be ignored.

#### Scenario: Unknown rule selector
- **WHEN** an otherwise supported snapshot contains a rule condition the auditor cannot interpret
- **THEN** the inventory preserves the condition and any coverage decision involving that rule requires more evidence

### Requirement: Separate observed and interpreted values
The auditor SHALL distinguish explicit field values, documented defaults for the supported shape, and unknown values.
It SHALL not treat a missing approval annotation as affirmative user approval or as a deny action.
It SHALL identify the interpretation source when a native default supplies a value.

#### Scenario: Approval annotation is absent
- **WHEN** a rule has no approval annotation
- **THEN** the auditor records that annotation as absent without inferring a reviewed decision or changing its action

### Requirement: Direction-correct transport evidence
The auditor SHALL preserve direction, protocol, destination, and port conditions separately.
An outgoing port condition SHALL mean a remote destination port; an incoming port condition SHALL mean a local receiving port.
External guidance about a local source port SHALL not become evidence for an equivalent outgoing remote-port restriction.

#### Scenario: Local source-port guidance
- **WHEN** submitted evidence describes a tunnel's local UDP source port and proposes an outgoing rule restricted to that remote port
- **THEN** the auditor records the mismatch and does not treat the source-port guidance as proof of coverage

### Requirement: Separate rule and profile state
The auditor SHALL preserve disabled state, approval annotation, profile membership, group state, and active-profile evidence as separate fields.
It SHALL classify a rule as disabled only when the supported native condition establishes that state.
An enabled rule in an inactive profile SHALL not become a disabled-clutter candidate for that reason.

#### Scenario: Enabled Work rule while Trusted is active
- **WHEN** an enabled rule belongs to inactive Work and the snapshot identifies Trusted as active
- **THEN** the rule remains enabled in the inventory and is not classified as disabled clutter

### Requirement: Evidence limits remain explicit
The auditor SHALL label the snapshot as saved configuration evidence, not as continuous live state.
It SHALL distinguish process and via selectors, vendor identity, certificate-chain conditions, build hashes, and unchecked helpers without claiming current executable verification.
It SHALL not infer endpoint ownership, current connectivity, or obsolescence from names, addresses, age, or use counts alone.

#### Scenario: Old low-use media allowance
- **WHEN** a saved media rule has a changing endpoint and a low historical use count
- **THEN** the auditor retains those observations but reports that current need and endpoint durability remain unproven

### Requirement: Read-only input boundary
The auditor SHALL leave supplied snapshots, plans, and evidence attachments unchanged.
It SHALL refuse repository-contained or symlink snapshot inputs and report a safe input error.
It SHALL read no adjacent files unless the caller explicitly supplies them as inputs.

#### Scenario: Snapshot path is a symlink
- **WHEN** the supplied snapshot path or one of its directory components is a symlink
- **THEN** the auditor refuses the input without following the link or reading a neighboring file
