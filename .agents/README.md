# Agent resources

These files define repository-specific policy for agents and reviewers.

| Path | Purpose |
| --- | --- |
| [Scope and publication](rules/scope-and-publication.md) | Scope, privacy, approval, and publication rules |
| [Identity and profiles](rules/identity-and-profiles.md) | Identity, profile, and subscription rules |
| [Evidence and validation](rules/evidence-and-validation.md) | Evidence and validation rules |
| [Daybreak adversary](agents/daybreak-adversary.md) | Independent read-only adversarial review contract |
| [Codex adapter](../.codex/agents/daybreak-adversary.toml) | Codex adapter for the Daybreak review contract |

The Daybreak contract is provider-neutral Markdown.
A harness must dispatch it through a native agent feature or adapter.
The file does not load itself or select a model by itself.

Codex loads the adapter from `.codex/agents/daybreak-adversary.toml`.
The adapter selects `gpt-daybreak-blue-latest` with high reasoning.
The adapter requests a read-only sandbox and tells the agent to load the canonical contract.
The active parent session can override inherited runtime permissions.
Verify the effective model and sandbox from runtime evidence before you report them.
