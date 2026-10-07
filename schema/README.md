# Experimental schemas

[Core schema](oars-core.schema.json) uses JSON Schema Draft 2020-12 and validates one Core record. [Binding schema](oars-binding.schema.json) wraps one Subject Binding or Authority Binding with `oars_version`. [Fixture schema](fixture.schema.json) validates repository example/test containers, including each contained Core record and binding.

The original separate schema was not supplied. These schemas are reconstructed from the uploaded HTML; see [decisions](../docs/DECISIONS.md). No canonical schema domain or `$id` is invented. Local relative references resolve within this directory. Enable date-time format assertions; format annotations alone are insufficient for this suite.

Schema validation cannot establish trust, enterprise meaning, conditional producer intent, historical uniqueness, interval ordering, or correct resolution. The semantic fixtures and resolver tests cover a limited explicit subset. Unknown optional fields are allowed to preserve extension behavior.
