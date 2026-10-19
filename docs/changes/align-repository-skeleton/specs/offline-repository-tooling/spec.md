# Offline repository tooling

## ADDED Requirements

### Requirement: Preserve the public boundary

Repository tooling MUST exclude private payloads from lint inputs and CI checkout.

#### Scenario: Run local lint with an initialized private submodule

- **WHEN** a contributor invokes the documented lint target
- **THEN** each linter receives only explicit public file paths
- **AND** the tooling does not initialize or inspect private payloads

### Requirement: Keep setup inactive

Repository setup MUST NOT install dependencies, activate hooks, or change firewall settings automatically.

#### Scenario: Run a documented Make target

- **WHEN** a contributor invokes validation or lint
- **THEN** missing tools cause a visible failure
- **AND** the target does not download tools or modify host configuration

### Requirement: Preserve the existing checks

The validation target MUST run the existing package validator and regression suite without weakening their assertions.

#### Scenario: Validate a public checkout

- **WHEN** the required Python version is available
- **THEN** validation reports the package checks and regression results
- **AND** CI uses a read-only token with private submodule checkout disabled

### Requirement: Record template provenance

The adaptation MUST identify its upstream revision, license, modifications, and intentionally omitted template functions.

#### Scenario: Review a later template update

- **WHEN** a maintainer compares this adaptation with upstream
- **THEN** the alignment document identifies the pinned revision and scope
- **AND** the existing private and policy boundaries remain explicit
