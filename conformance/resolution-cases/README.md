# Deterministic resolution vectors

Each JSON file is a repository fixture container, not a Core record. `records` contains accepted Core statements. `query` supplies exact Subject, Context, Authority, and effective time. `expected.result` is one of the six Core outcomes. Optional bindings, fixture trust labels, `expected_mapping`, and `expected_constraints` test correlation and constraint reporting separately.

The suite covers all outcomes, human-before-policy precedence, empty grants, absence versus deny, future and expired state, historical supersession, later-issued corrections, competing corrections, ambiguous overlap, multi-context reuse, vendor migration, late evidence, untrusted/ambiguous bindings, capability without grant, delegation without inferred grants, exact cutover, timestamp offsets, missing history, and cycles.

The runner checks every permutation of record and binding order. No fixture can depend on input order. All convention-dependent results use the [documented laboratory rules](../../docs/DECISIONS.md). The `allow_missing_history` switch in one test isolates RFC Appendix A grant classification; default full-history cases return INDETERMINATE for unresolved links.

`expected_mapping.status` is a repository diagnostic, not an extra Core result vocabulary. Binding failures never upgrade authority or prove identity. Synthetic `trusted_asserted_by` strings simulate an external trust decision solely for test execution.
