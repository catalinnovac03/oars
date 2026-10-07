# Intentionally invalid records

These files are valid JSON syntax. They are intentionally invalid at the layer named in [manifest.json](manifest.json). Each manifest entry records the instance JSON Pointer, validation rule, and explanation. A schema-layer fixture must fail at the documented path/rule. A semantic-layer fixture must pass the schema and fail the corresponding repository semantic check.

Schema cases cover missing scope, wrong version, malformed timestamp, missing authority ID, a string instead of a boolean, and an unsupported relationship type. Semantic cases cover interval ordering, duplicate authority keys, and self-correction. Those semantic conventions are explicitly documented in [DECISIONS.md](../../docs/DECISIONS.md); not every one is a separately stated source MUST.

Resolver-level problems such as competing records, unresolved history, and cyclic relationships live in [resolution cases](../resolution-cases/README.md), since individually well-formed records can still yield INDETERMINATE.
