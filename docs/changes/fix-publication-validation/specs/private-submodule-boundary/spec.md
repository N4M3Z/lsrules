# Private submodule boundary

## ADDED Requirements

### Requirement: Exact private submodule declaration

The package check MUST permit only the root `.gitmodules` declaration for `lsrules-private` at path `private`.
Its URL MUST be `https://github.com/N4M3Z/lsrules-private.git`.
The declaration MUST use the supported canonical three-line form without other sections, keys, or values.
Any other `.gitmodules`, nested public `.git`, or nested public `.jj` entry MUST fail validation.

#### Scenario: Declaration contains another URL

- **WHEN** the root submodule declaration changes its URL or adds another setting
- **THEN** the package check fails without traversing private payload

### Requirement: Private payload is never public validation input

Public traversal MUST prune the root `private` entry before it descends into that entry.
Public document references MUST NOT resolve or inspect any path that enters the private boundary.
The check MUST reject a private root that is a symlink, broken symlink, or ordinary file.
Without the exact declaration, any root `private` entry MUST fail validation.
With the declaration, an absent or empty private directory MUST pass without invoking Git.
A populated ordinary directory MUST NOT receive an exception.

#### Scenario: Declared private checkout is not initialized

- **WHEN** the exact declaration exists and `private` is absent or empty
- **THEN** validation uses the standard library only and records no claim of an initialized gitlink

#### Scenario: Ordinary directory uses the private name

- **WHEN** a populated directory lacks valid submodule evidence
- **THEN** validation fails without reading that directory's payload

#### Scenario: Public document references private payload

- **WHEN** a local reference enters the private boundary, including an encoded or case-variant path
- **THEN** validation rejects the reference before resolving or inspecting its target

### Requirement: Populated private checkout requires Git evidence

A populated private checkout MUST have a regular gitfile with the exact target `../.git/modules/lsrules-private`.
The parent Git directory and each target directory component MUST be real directories without symlinks.
Read-only Git evidence MUST identify both expected worktree roots and resolve the child HEAD to a commit.
The check MUST reject metadata symlinks, shared-directory redirects, object alternates, and configuration includes before Git runs.
The parent index MUST contain exactly one stage-zero mode-160000 entry at `private`, matching that commit.
Any missing, failed, mismatched, or additional evidence MUST fail validation without a fallback to uninitialized state.

#### Scenario: Parent index points to another commit

- **WHEN** the private gitlink commit differs from the child HEAD commit
- **THEN** the private boundary check fails without scanning the private payload

#### Scenario: Git metadata redirects a probe

- **WHEN** parent or child metadata contains an unsupported redirect or symlink
- **THEN** validation fails before invoking Git

#### Scenario: Initialized checkout contains private data and symlinks

- **WHEN** the exact boundary and Git evidence pass
- **THEN** public validation does not read or traverse any private payload file or payload symlink

### Requirement: Git evidence stays read-only and offline

Git MUST run only for a populated private checkout.
The check MUST invoke only the specified `rev-parse` and `ls-files` commands.
It MUST clear inherited Git redirection variables and disable optional locks, prompts, lazy fetch, and network transports.
It MUST suppress external filesystem monitors for these reads and MUST NOT disable commit or push hooks.
It MUST NOT create repositories, commits, fixture commits, remotes, pushes, or releases.

#### Scenario: Environment redirects the Git index

- **WHEN** inherited environment variables specify another Git directory, worktree, or index
- **THEN** the evidence command ignores those variables and checks only the selected local checkout
