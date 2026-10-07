# Conformance and executable checks

Core Producer, Core Consumer, Binding Producer, and Profile Implementation are the Core conformance targets. Claims must identify `0.4-draft` and the applicable class/profile. A passing schema or repository suite is not proof of trust or full normative conformance.

- [Valid fixtures](valid/README.md) cover minimal, approved, extension-bearing, complete example, and binding documents.
- [Invalid fixtures](invalid/README.md) and the [manifest](invalid/manifest.json) identify exact expected validation layers, paths, and rules.
- [Resolution cases](resolution-cases/README.md) test the Core result vocabulary and separately labeled repository conventions.

Run the [Python validation command](../reference/python/README.md). All JSON documents are parsed strictly; schemas are checked against the metaschema; record examples and nested records/bindings are validated; semantic failures are checked separately; deterministic vectors are tested in every input permutation; local links and fragments are checked. See [VALIDATION.md](../docs/VALIDATION.md) for the run results.

Manual review remains necessary for implementation-independent IDs, durable authority meaning, valid issuer authority, authenticity, unknown-content preservation in an actual pass-through system, and an approved-state producer's obligation to provide an Assessment decision. The repository harness does not claim to certify these properties.
