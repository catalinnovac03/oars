# Profiles

Profiles may map Core to ecosystems such as OpenTelemetry, A2A, MCP, OASF, or vendor platforms. No profile is implemented or adopted by this bundle. The source's `OARS-OpenTelemetry/0.1-draft` conformance example is illustrative, not evidence that such a profile exists.

A profile must identify its own version and supported exact Core version, describe targets and references, and preserve Core object and resolution meanings. It may add mappings, fields, target types, and processing without converting capability metadata into enterprise grants. `oars.subject.id` and `oars.context.id` are correlation claims, not identity or Context proof.

Proposals should specify serialization, scope selection, binding validity, external trust assumptions, unknown-field behavior, security/privacy concerns, and examples plus conformance cases. Subject/Context identity must survive implementation migration. Possible future binding, OpenTelemetry, and A2A RFCs remain proposals, not published standards.
