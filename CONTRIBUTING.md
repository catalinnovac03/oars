# Contributing to OARS

OARS is a proposed open standard, currently at `0.4-draft` with Public Review Draft status. Technical review, independent implementation, and interoperability results are welcome. Use issues for interoperability questions and proposals, and pull requests for concrete specification or implementation changes.

Challenge the Core model with concrete use cases, identify ambiguous requirements, and compare independently developed implementations against the shared fixtures. Report implementation versions, inputs, observed results, and any differences from the RFC or reference harness. An implementation report should identify its tested scope and limitations.

## Propose a change

Describe the problem, the expected behavior, and a small example that demonstrates it. For a normative change, identify the affected RFC sections and compatibility impact. Link existing issues when relevant.

Edit [RFC 0001](rfcs/0001-oars-core.md) as the canonical specification. Keep the schema, examples, resolution fixtures, and [decision log](docs/DECISIONS.md) consistent in the same change. Record substantive draft changes in [CHANGELOG.md](CHANGELOG.md) and the RFC history. Preserve archived drafts and published record identities.

## Validate a change

Follow the [local validation instructions](README.md#validate-locally). Pull requests run the same checks in GitHub Actions on Python 3.10 and 3.14. Provide a fixture for new observable behavior, and document the intended failure for any invalid example.

Keep implementation identifiers in bindings. Preserve Subject × Context semantics, the distinction between capability and authority, and the rule that absence of a grant is not an explicit deny. Profiles must preserve Core meanings and resolution results.

## Discussion and sensitive information

Discuss technical claims respectfully and support them with examples or evidence. Use synthetic records; avoid posting private enterprise data, credentials, customer information, or private assessment evidence. Use the [security reporting route](SECURITY.md) for vulnerabilities.

Licensing, named editors, formal decision authority, and conduct-reporting responsibilities remain [open publication decisions](docs/PUBLICATION.md). This document establishes no contributor license agreement, governance organization, response deadline, or named approver.
