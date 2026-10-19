# Third-party notices

## Adopted decision record

The Spec-Driven Change Lifecycle decision comes from [runedeck/deck](https://github.com/runedeck/deck).
Its upstream source is CORE-0019 at commit `1e016dbe972ce07d5fce9b44fc2928680b5c6d2b`.
The upstream project specifies EUPL-1.2. This package includes the unchanged [license text](LICENSE).

The following files retain that upstream license and attribution:

- [LSR-0001 Spec-Driven Change Lifecycle](<docs/decisions/LSR-0001 Spec-Driven Change Lifecycle.md>).
- Its recorded replacement blocks under `docs/decisions/.provenance/replacements/`.
- The exact upstream source under `docs/decisions/.provenance/sources/`.

LSR-0001 adapts CORE-0019 for this repository and its native `docs/` tree.
The adoption record dates those modifications to 2026-09-20 and preserves the transformation details.
The publication copy identifies the reviewer by public handle. The original reviewer record remains in private evidence.
The source copy remains unchanged. The original decision retains its author attribution.
The publication preparation added this notice and the upstream license copy on 2026-10-17.

## Repository template adaptation

The repository tooling adapts [runedeck/skeleton](https://github.com/runedeck/skeleton) at commit `62e1f6674ac7c1d248d71eaa2660ebda600c3ef0`.
That upstream project uses EUPL-1.2. The existing [license text](LICENSE) remains unchanged.

The adaptation dated 2026-10-18 uses `templates/base/`, `templates/python/`, and `templates/tool/`.
The document schemas retain the upstream bytes.
The editor configuration adds exceptions for private and adopted evidence.
The Vale style files retain their upstream rules with an added snapshot comment.
The Makefile, lint configurations, contribution guide, pull request template, and quality workflow adapt the template for this package.
The README retains the tool template structure with package-specific content.

See [template alignment](docs/skeleton-alignment.md) for the included files, maintenance method, and omitted template functions.
The adaptation preserves the existing public license, private boundary, and author identity.

## Referenced blocklists

The catalog contains source metadata and links. It contains no upstream blocklist entries or generator code.
Each upstream source retains its own terms. A generator license does not establish rights to its input data.
See the [source review](catalog/review-2026-10-17.md) before copying or redistributing any list contents.

## Original package files

The owner selected EUPL-1.2 for the original package files on 2026-10-17.
The [license](LICENSE) applies to those files and the adopted material identified above.
Retain the upstream attribution and modification notices in any publication package.
The catalog links external lists. The package license grants no additional rights to those lists or private companion data.
