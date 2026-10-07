# TypeScript implementation guidance

A TypeScript implementation is not yet available. This directory provides implementation guidance for the Core model and shared conformance fixtures. The [Python harness](../python/README.md) provides an executable reference for comparison.

An implementation should load [the schemas](../../schema/README.md) with Draft 2020-12 and date-time format support, preserve unknown optional data, and implement the [RFC processing model](../../rfcs/0001-oars-core.md#processing-model). Use exact Subject × Context lookup, effective-time history, and the six exact result strings. Do not use array order, issuance recency, or grant union to resolve conflicts.

Run the same [resolution vectors](../../conformance/resolution-cases/README.md), including permutations, offsets, migration cutover, historical correction, missing grants, and untrusted binding mappings. Match the documented [harness conventions](../../docs/DECISIONS.md) when comparing to Python. Decide and disclose timestamp precision and leap-second handling; do not silently inherit JavaScript Date truncation. Policy evaluation, signature verification, and runtime authorization are outside this scaffold.
