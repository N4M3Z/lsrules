# Identity and profiles

- Prefer a verified stable vendor Code ID for signed software.
- Use a build hash only when one build must remain fixed.
- Use Path without Identity Check only for a documented, frequently updated unsigned helper.
- Restrict that helper with a signed parent, required hosts, protocols, ports, directions, and profiles.
- Record each unchecked helper exception in policy metadata.
- Never weaken every unsigned CLI because one helper updates frequently.
- Preserve parent Code IDs and signatures during helper edits.
- Preserve all existing hosts, ports, directions, actions, and profiles unless the user changes the scope.
- A profile is host-local state.
- A remote subscription is global unless native documentation proves profile scope.
- Do not describe a global subscription as a Work-only rule.

