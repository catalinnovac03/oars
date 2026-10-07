# Design decisions and open questions

[RFC 0001](../rfcs/0001-oars-core.md) is the canonical specification. This document records experimental serialization choices, reference-harness conventions, and issues to resolve before a stable wire contract. The exact Core version is **0.4-draft**.

## Experimental JSON serialization

The schema implements the Core model and examples in RFC 0001. Required top-level fields follow Section 2. Nested object shapes and fixture wrappers are experimental serialization choices; compatibility with other draft schema artifacts has not been established.

- `scope.id`, Subject/Context IDs, `effective.from`, `grants`, and grant `authority_ref` are required by this repository schema to make the documented model executable.
- Assessment is required, but `decision` remains optional structurally because the Core draft requires it specifically when representing an approved state. The schema does not define a closed decision vocabulary. The producer must include a decision when making that claim; a schema cannot infer the producer's unstated intent.
- IDs/references are nonempty strings; URI syntax is not required. Technical target refs may be vendor-local strings. No canonical `$id` or domain is assigned.
- Unknown fields remain allowed; extensions are recommended, not mandatory. This means typo detection is incomplete by design.
- The binding document wrapper and multi-record fixture container are repository conveniences, not a newly standardized Core transport. Binding reference/evidence fields reuse the Assessment reference shape as an experimental convention.
- The Core model includes implementation and/or principal bindings but demonstrates only `implementation`. This schema covers that illustrated form; a principal-only interoperable serialization remains open.

## Deterministic harness conventions (not additional settled 0.4 requirements)

1. Effective intervals are half-open `[from, until)`, with an absent end unbounded. Empty/reversed intervals are rejected. The Core draft does not explicitly settle endpoint inclusion; this convention makes cutover deterministic.
2. Queries evaluate effective time against the accepted input dataset. Issued time is not a filter. A later-issued valid correction can therefore affect an earlier effective-time query. A separate “known as of” transaction-time query is not standardized or implemented.
3. String identity comparison is exact and case-sensitive, without aliasing or URI normalization. A Subject/Context pair must resolve to one scope ID, and a scope ID must not identify conflicting pairs in the dataset.
4. Complete history is expected by default. Missing relationship targets, cycles, different-scope history, non-later issue times, and duplicate IDs cause INDETERMINATE. One example-record test explicitly permits an omitted predecessor to isolate grant classification; it is not proof of complete historical resolution.
5. For executable correction fixtures, correcting and corrected records have identical effective intervals. Partial corrections remain unspecified and return INDETERMINATE in the harness. Supersession takes effect only while the superseder is effective. Active successors suppress their available transitive predecessors; ended superseders do not permanently revoke a predecessor.
6. Competing surviving records return INDETERMINATE, even when envelopes happen to agree. The Core draft does not define record merging or a tie-breaker. Neither latest-issued-wins nor grant union is used. Duplicate authorities within one envelope are rejected by the harness.
7. Binding correlation is a separate output. An ambiguous mapping is INDETERMINATE in that output; it does not change the independently resolved grant result, following RFC Section 11 step 9. This makes explicit the tension with RFC Section 15's broader ambiguity wording. External enforcement must evaluate both outputs as appropriate.
8. Fixture `trusted_asserted_by` values stand in for an externally established binding trust decision. Strings alone are not authentication. Core record acceptance/trust is a precondition of the harness; no real trust validation is implemented.
9. RFC 3339 offsets and fractional seconds are supported for ordinary timestamps. Python's datetime harness does not support leap-second values; that limitation is separate from the Core timestamp requirement. Assessment expiration does not change the Core grant result. External policy is never evaluated, and qualifying human authorization is never presumed.

## Open before stabilizing a wire contract

Settle serialization compatibility, interval boundaries, partial corrections, history completeness, competing equivalent states, knowledge-time querying, leap seconds, binding serialization and principal mappings, trust packaging, and assessment decision vocabularies. These items remain open for technical review. No production conformance or interoperability certification is claimed.
