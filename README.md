# OARS — Open Authority Record Standard

[![Validate OARS](https://github.com/catalinnovac03/oars/actions/workflows/validate.yml/badge.svg)](https://github.com/catalinnovac03/oars/actions/workflows/validate.yml)

OARS is a **proposed open, vendor-neutral standard** for representing the enterprise-granted authority of AI systems and agents. It carries governance identity, context, and authority across platforms.

**Capability describes what an AI system can do. Authority describes what the enterprise has authorized it to do.** OARS connects durable governance meaning to changing implementations through effective-dated bindings.

**Status: Public Review Draft · Version: 0.4-draft**

**Author and editor: Catalin Novac.** See the [preferred citation](docs/CITATION.md) when referencing the proposal.

Start with [RFC 0001: OARS Core](rfcs/0001-oars-core.md), the canonical project specification.

## The model

| Concept | Purpose |
|---|---|
| Governance Scope | The **Subject × Context** pair being governed. |
| Authority Envelope | Enterprise grants and their human-authorization or external-policy constraints. |
| Assessment | The governance decision and references supporting the envelope. |
| Subject Binding | An effective-dated mapping from scope to technical implementation. |
| Authority Binding | An effective-dated mapping from enterprise authority to technical capability. |

Issued time and effective time remain distinct. Historical resolution preserves supersession and correction history. An authority absent from an envelope is `NOT_GRANTED_BY_ENVELOPE`; absence is not an explicit deny.

## Examples

- [Claims Assistant](rfcs/0001-oars-core/claims-assistant.json): a complete record with grants, assessment references, accountability, and history metadata.
- [Microsoft-to-AWS migration](rfcs/0001-oars-core/migration-microsoft-aws.json): stable governance identity and authority across a platform cutover.
- [Retrospective correction](rfcs/0001-oars-core/retrospective-correction.json): a later-issued correction that retains the original historical statement.

## Validate locally

Use Python 3.10 or later, then run from the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r reference/python/requirements.txt
.venv/bin/python tools/validate.py
```

On Windows, use the Python executable under `.venv/Scripts/` in place of `.venv/bin/python`.

Validation checks JSON syntax, schemas, examples, expected invalid records, deterministic authority-resolution cases, and local documentation links. The same checks run on pushes and pull requests through GitHub Actions.

## Explore the repository

| Directory | Contents |
|---|---|
| [rfcs](rfcs/0001-oars-core.md) | Canonical Core specification and worked examples. |
| [schema](schema/README.md) | Draft Core, binding, and fixture schemas. |
| [conformance](conformance/README.md) | Valid/invalid records and deterministic resolution vectors. |
| [reference/python](reference/python/README.md) | Executable reference harness. |
| [reference/typescript](reference/typescript/README.md) | Implementation guidance and scaffold. |
| [profiles](profiles/README.md) | Guidance for independently versioned ecosystem mappings. |
| [docs](docs/README.md) | Design decisions, open review items, and validation details. |

## Status and participation

OARS is open for public review, independent implementation, and interoperability testing. Review the specification, challenge the authority model, implement it independently, and contribute interoperability results.

- [Review RFC 0001](rfcs/0001-oars-core.md) and its [open design questions](docs/DECISIONS.md).
- [Discuss a proposal or report a problem](https://github.com/catalinnovac03/oars/issues).
- Build an independent implementation against the [conformance cases](conformance/README.md) and report disagreements or portability results.

The draft leaves some serialization and resolution details under review; the reference harness documents its experimental conventions. Breaking changes may occur before 1.0. Independent interoperability and adoption have not yet been demonstrated. The proposal does not claim IETF publication or standards-body approval.

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose specification changes or implementation fixes, and [SECURITY.md](SECURITY.md) for security reporting.

**License: [Apache 2.0](LICENSE).** The specification, documentation, schemas, examples, fixtures, and reference code use the same license. Formal governance and any canonical domain remain unassigned; see [publication decisions](docs/PUBLICATION.md).
