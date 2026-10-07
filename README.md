# OARS — Open Authority Record Standard

[![Validate OARS](https://github.com/catalinnovac03/oars/actions/workflows/validate.yml/badge.svg)](https://github.com/catalinnovac03/oars/actions/workflows/validate.yml)

OARS is a vendor-neutral standard for recording the enterprise-granted authority of AI systems and agents. It represents governance identity and context across platforms.

**Capability describes what an AI system can do. Authority describes what the enterprise has authorized it to do.** OARS connects durable governance meaning to changing implementations through effective-dated bindings.

**Start with [RFC 0001: OARS Core](rfcs/0001-oars-core.md).** The current version is `0.4-draft`, published as an experimental project RFC for public review and interoperability testing.

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
| [schema](schema/README.md) | Experimental Core, binding, and fixture schemas. |
| [conformance](conformance/README.md) | Valid/invalid records and deterministic resolution vectors. |
| [reference/python](reference/python/README.md) | Executable experimental reference harness. |
| [reference/typescript](reference/typescript/README.md) | Implementation guidance and scaffold. |
| [profiles](profiles/README.md) | Guidance for independently versioned ecosystem mappings. |
| [docs](docs/README.md) | Design decisions, open review items, and validation details. |

## Status and participation

The JSON Schema and reference harness implement an experimental serialization and resolution model. [Design decisions and open questions](docs/DECISIONS.md) document the current conventions and issues to settle before a stable wire contract. Breaking changes may occur before 1.0. This is a public project RFC, with no claim of IETF publication or standards-body approval.

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose specification changes or implementation fixes, and [SECURITY.md](SECURITY.md) for security reporting.

**License TODO: no license has been selected.** Editor identities, formal governance, and any canonical domain remain unassigned; see [publication decisions](docs/PUBLICATION.md).
