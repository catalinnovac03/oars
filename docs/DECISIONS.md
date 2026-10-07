# Provenance, editorial decisions, and open questions

The supplied October 2026 HTML is the semantic source. [Its snapshot](../provenance/OARS_0.4_Standards_Grade_Public_Review_Draft.html) is retained unchanged for audit; [RFC 0001](../rfcs/0001-oars-core.md) is now canonical within this repository. The project's exact declared version is **0.4-draft**. The prior conversation selected a numbered public project RFC, with schema and examples early. It did not select a license or governance identities.

## Reconstructed schema, not a recovered schema

The HTML mentions `oars-core-0.4.schema.json`, but that artifact was not uploaded. This repository's schema is derived from prose and examples. Required top-level fields come directly from source Section 4. Nested object shapes are experimental serialization choices inferred from the source examples. They must not be described as byte-compatible with the unavailable original schema.

- `scope.id`, Subject/Context IDs, `effective.from`, `grants`, and grant `authority_ref` are required by this repository schema to make the documented model executable.
- Assessment is required, but `decision` remains optional structurally because the source requires it specifically when representing an approved state. The schema does not invent a closed decision vocabulary. The producer must include a decision when making that claim; a schema cannot infer the producer's unstated intent.
- IDs/references are nonempty strings, not an invented URI-only identity regime. Technical target refs may be vendor-local strings. No canonical `$id` or domain is assigned.
- Unknown fields remain allowed; extensions are recommended, not mandatory. This means typo detection is incomplete by design.
- The binding document wrapper and multi-record fixture container are repository conveniences, not a newly standardized Core transport. Binding reference/evidence fields reuse the source Assessment reference shape as an experimental convention.
- The source mentions implementation and/or principal bindings but demonstrates only `implementation`. This schema covers that illustrated form; a principal-only interoperable serialization remains open.

## Deterministic harness conventions (not additional settled 0.4 requirements)

1. Effective intervals are half-open `[from, until)`, with an absent end unbounded. Empty/reversed intervals are rejected. The source does not explicitly settle endpoint inclusion; this convention makes cutover deterministic.
2. Queries evaluate effective time against the supplied accepted dataset. Issued time is not a filter. A later-issued valid correction can therefore affect an earlier effective-time query. A separate “known as of” transaction-time query is not standardized or implemented.
3. String identity comparison is exact and case-sensitive, without aliasing or URI normalization. A Subject/Context pair must resolve to one scope ID, and a scope ID must not identify conflicting pairs in the dataset.
4. Complete history is expected by default. Missing relationship targets, cycles, different-scope history, non-later issue times, and duplicate IDs cause INDETERMINATE. One source-example test explicitly permits an omitted predecessor to isolate grant classification; it is not proof of complete historical resolution.
5. For executable correction fixtures, correcting and corrected records have identical effective intervals. Partial corrections remain unspecified and return INDETERMINATE in the harness. Supersession takes effect only while the superseder is effective. Active successors suppress their available transitive predecessors; ended superseders do not permanently revoke a predecessor.
6. Competing surviving records return INDETERMINATE, even when envelopes happen to agree. The source does not define record merging or a tie-breaker. Neither latest-issued-wins nor grant union is used. Duplicate authorities within one envelope are rejected by the harness.
7. Binding correlation is a separate output. An ambiguous mapping is INDETERMINATE in that output; it does not change the independently resolved grant result, following source Section 11 step 9. This makes explicit the tension with source Section 15's broader ambiguity wording. External enforcement must evaluate both outputs as appropriate.
8. Fixture `trusted_asserted_by` values stand in for an externally established binding trust decision. Strings alone are not authentication. Core record acceptance/trust is a precondition of the harness; no real trust validation is implemented.
9. RFC 3339 offsets and fractional seconds are supported for ordinary timestamps. Python's datetime harness does not support leap-second values; that limitation is separate from the Core timestamp requirement. Assessment expiration does not change the Core grant result. External policy is never evaluated, and qualifying human authorization is never presumed.

## Open before stabilizing a wire contract

Recover/reconcile the original schema; decide interval boundaries, partial corrections, history completeness, competing equivalent states, knowledge-time querying, leap seconds, binding serialization and principal mappings, trust packaging, and assessment decision vocabularies. These are review items, not fabricated standards decisions. No production conformance or interoperability certification is claimed.
