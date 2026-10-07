# RFC 0001: Open AI Authority Record Standard (OARS) Core

| Field | Value |
|---|---|
| Status | Experimental public-review project RFC |
| Core version | `0.4-draft` |
| Publication date | October 2026 |
| Repository edition | 2026-10-07 |
| Authors / editors | TODO — not assigned |
| Maintainers | TODO — not assigned |
| Target | Experimental vendor-neutral interoperability specification |
| Canonical source | This Markdown file in the repository |
| Canonical public URL | [RFC 0001 in the project repository](https://github.com/catalinnovac03/oars/blob/main/rfcs/0001-oars-core.md) |
| License | TODO — not selected; no LICENSE included |

This **project RFC** defines the OARS Core model, experimental JSON serialization, and authority-resolution processing. It is the canonical specification for `0.4-draft`. [Design decisions and open questions](../docs/DECISIONS.md) document experimental conventions and unresolved details. This document does not claim IETF publication.

## Contents

- [Introduction](#introduction)
- [Core data model and schema](#core-data-model)
- [Terminology](#conventions-and-terminology)
- [Governance Scope](#governance-scope), [Authority Envelope](#authority-envelope), [Assessment](#assessment)
- [Bindings](#bindings), [time and history](#temporal-and-record-model)
- [Processing model](#processing-model), [conformance](#conformance)
- [Security](#security-considerations), [versioning](#versioning-and-compatibility)
- [Worked repository examples](#repository-examples)

<a id="abstract"></a>

## Abstract

OARS defines a portable representation of the governance identity, context, and enterprise-granted authority of an AI system or agent, independent of the platforms that implement, execute, or observe it. OARS separates durable governance semantics from vendor resource identity and technical capability, then reconnects them through explicit, effective-dated bindings. The specification is designed to complement agent discovery, tool protocols, policy engines, identity systems, observability, bills of materials, and GRC assessment formats rather than replace them.

<a id="status-of-this-document"></a>

## Status of This Document

This document is Draft 0.4 for public review and interoperability experiments. The Core semantics and processing model are experimental. Implementations **MAY** be built against this draft, but conformance claims **MUST** identify the exact draft version. Breaking changes **MAY** occur before OARS 1.0. Editor identities, licensing, and formal project governance remain open publication decisions.

<a id="introduction"></a>

## 1. Introduction

Enterprise AI governance spans heterogeneous agent platforms, clouds, GRC systems, policy engines, gateways, identity providers, and observability stacks. Those systems can describe useful local facts, but durable governance meaning is often coupled to the platform where an agent is registered or executed. OARS addresses the narrower interoperability problem of carrying enterprise governance identity and authority semantics across those systems.

<a id="core-data-model"></a>

## 2. Core Data Model

The following minimal JSON record shows the complete top-level shape. It makes no approved-state claim; an approved-state Producer must include an Assessment decision.

```json
{
  "oars_version": "0.4-draft",
  "record": {
    "id": "urn:example:record:minimal",
    "issued_at": "2027-01-01T00:00:00Z"
  },
  "scope": {
    "id": "urn:acme:oars:scope:claims-eu-production",
    "subject": {
      "id": "urn:acme:ai-system:claims-assistant",
      "type": "ai_system"
    },
    "context": {
      "id": "urn:acme:context:claims-eu-production",
      "purpose_ref": "urn:acme:use-case:claims-assistance"
    }
  },
  "effective": {
    "from": "2027-01-01T00:00:00Z"
  },
  "authority_envelope": {
    "grants": []
  },
  "assessment": {}
}
```

### 2.1 Record envelope

```yaml
oars_version: "0.4-draft"
record:
  id: "urn:acme:oars:record:claims:002"
  issued_at: "2027-03-01T00:00:00Z"
  issued_by: "urn:acme:ai-governance"
```

- A Core record MUST contain oars\_version, record.id, record.issued\_at, scope, effective, authority\_envelope, and assessment.

- A published record SHOULD be semantically immutable.

- A Producer MUST NOT change the meaning of an existing record identifier after publication.

| Object | Normative purpose |
| --- | --- |
| Governance Scope | Durable Subject x Context pair to which governance applies. |
| Authority Envelope | Authorities granted to that scope, with narrowly defined OARS constraints. |
| Assessment | Governance decision and validity supporting the envelope. |
| Subject Binding | Effective-dated mapping from Governance Scope to implementation/principal. |
| Authority Binding | Effective-dated mapping from enterprise Authority to technical semantics. |

### Normative field tables for this experimental repository serialization

The field tables define requiredness for this experimental JSON serialization. Read them together with the [schema documentation](../schema/README.md) and [open design decisions](../docs/DECISIONS.md). All objects permit unknown optional fields. Nonempty strings do not by themselves prove identity or authority.

| Field | Type | Required | Meaning |
|---|---|---|---|
| `oars_version` | string | Yes | Exactly `0.4-draft`. |
| `record` | object | Yes | Immutable statement metadata. |
| `scope` | object | Yes | Governance Scope = Subject × Context. |
| `effective` | period | Yes | Governance state validity, distinct from issuance. |
| `authority_envelope` | object | Yes | Explicit grants and narrow Core constraints. |
| `assessment` | object | Yes | Supporting governance decision/validity/references. |
| `accountability` | object array | No | Entries with required `role` and `party_ref` strings. |
| `extensions` | object | No | Optional extension content; does not redefine Core. |

| Object / field | Type | Required | Meaning |
|---|---|---|---|
| `record.id` | string | Yes | Published statement identity; do not reuse with changed meaning. |
| `record.issued_at` | date-time | Yes | RFC 3339 issuance time. |
| `record.issued_by` | string | No | Claimed issuer; not proof of trust. |
| `record.relationship` | object | No | Required `type` (`supersedes` or `corrects`) and `ref` to prior record. |
| `scope.id` | string | Yes | Stable identifier for the pairing. |
| `scope.subject` | object | Yes | Required `id`; optional `type` string. Implementation-independent. |
| `scope.context` | object | Yes | Required `id`; optional `purpose_ref` string. |
| `period.from` | date-time | Yes | Start of state or binding validity. |
| `period.until` | date-time | No | End, if known; see interval convention. |
| `authority_envelope.grants` | grant array | Yes | Empty is allowed; absence of A is not explicit deny. |
| `grant.authority_ref` | string | Yes | Durable enterprise authority, not vendor capability. |
| `grant.human_authorization` | object | No | If present, required boolean `required`; true constrains the grant. |
| `grant.policy_refs` | string array | No | External constraints; not evaluated by Core. |
| `authority_envelope.delegation` | object | No | Required `permitted` boolean; optional `delegate_refs` string array and `redelegation` boolean. No transitive or grant-level inference. |
| `assessment.decision` | string | Conditional | Required for a represented approved state; not universally schema-required. No closed decision vocabulary is defined. |
| `assessment.effective` | period | No | Assessment validity; expiry is not an automatic deny. |
| `assessment.references` | reference array | No | External evidence, with required `rel`, `ref` and optional `type` strings. |

| Binding field | Type | Required | Meaning |
|---|---|---|---|
| `scope_ref` | string | Yes | Governance Scope being mapped. |
| Subject Binding `implementation` | target | Yes | Technical implementation using the illustrated binding shape. |
| Authority Binding `authority_ref` | string | Yes | Enterprise authority being mapped. |
| Authority Binding `target` | target | Yes | Technical skill, tool, capability, or runtime semantic. |
| target `type`, `ref` | strings | Yes | Ecosystem target type and identifier; no closed vendor registry. |
| `effective` | period | Yes | Mapping validity. |
| `asserted_by` | string | No | Claimed asserter; SHOULD be identified for significant mappings. |
| `references` | reference array | No | Experimental evidence representation; significant bindings SHOULD identify supporting evidence. |

The standalone [binding document schema](../schema/oars-binding.schema.json) uses `oars_version` and exactly one of `subject_binding` or `authority_binding`. This wrapper and [fixture containers](../schema/fixture.schema.json) are repository serialization conveniences, not a new Core transport.

### Machine-readable artifacts

Use the [Core JSON Schema](../schema/oars-core.schema.json) and the [complete Claims Assistant record](0001-oars-core/claims-assistant.json). Core records validate individually; scenario files contain records and bindings in a documented fixture wrapper. JSON Schema checks structure, not issuer trust, durable business meaning, or full temporal history.

<a id="conventions-and-terminology"></a>

## 3. Conventions and Terminology

### 3.1 Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described by BCP 14 when, and only when, they appear in all capitals. [RFC2119] [RFC8174]

### 3.2 Defined terms

| Term | Definition |
| --- | --- |
| Subject | The durable enterprise AI system or agent being governed. |
| Context | The durable governance scope in which the Subject operates, such as a business use context. |
| Governance Scope | The Subject x Context pair used to resolve applicable OARS governance state. |
| Authority | A durable governance semantic representing what the enterprise has authorized, distinct from technical capability. |
| Authority Envelope | The set of authority grants and OARS-defined constraints effective for a Governance Scope. |
| Assessment | The governance decision supporting an Authority Envelope. |
| Subject Binding | An effective-dated mapping from Governance Scope to technical implementation and/or runtime principal. |
| Authority Binding | An effective-dated mapping from enterprise Authority to a technical capability, tool, skill, or runtime semantic. |
| Producer | An implementation that emits OARS Core records. |
| Consumer | An implementation that interprets OARS Core records. |
| Binding Producer | An implementation that emits Subject Bindings or Authority Bindings. |
| Profile | A specification that maps OARS Core semantics to another standard or ecosystem without redefining Core semantics. |

<a id="architecture-and-scope"></a>

## 4. Architecture and Scope

OARS Core standardizes governance semantics above changing implementations. It does not standardize execution transport.

### 4.1 Non-goals

- Agent discovery, routing, or communication transport.

- Tool invocation or tool schema definition.

- Policy definition, policy evaluation, or explicit deny semantics.

- Telemetry, traces, prompts, runtime event formats, or evidence storage.

- Identity issuance, authentication, authorization enforcement, or attestation.

- GRC workflow, remediation, ticketing, risk scoring, regulatory classification, or control testing.

- A universal business-action or capability ontology.

- AI/ML bill-of-materials modeling.

| OARS Core | External / referenced systems |
| --- | --- |
| Governance Scope | Agent registries, CMDBs, runtime identities |
| Authority Envelope | Policy engines, tool schemas, capability taxonomies |
| Assessment decision + validity | OSCAL/GRC assessment evidence and workflows |
| Subject Binding | Vendor agent resources, IAM/workload principals |
| Authority Binding | A2A/OASF/MCP/vendor skills and tools |
| Temporal governance state | OpenTelemetry/runtime evidence |

<a id="governance-scope"></a>

## 5. Governance Scope

```yaml
scope:
  id: "urn:acme:oars:scope:claims-eu-production"
  subject:
    id: "urn:acme:ai-system:claims-assistant"
    type: "ai_system"
  context:
    id: "urn:acme:context:claims-eu-production"
    purpose_ref: "urn:acme:use-case:claims-assistance"
```

- The canonical Subject identifier MUST be implementation-independent.

- A Context identifier MUST distinguish materially different governance scopes.

- A Consumer MUST NOT infer Context solely from a runtime principal or vendor resource ID.

- A Governance Scope identifier SHOULD be stable for the lifetime of the Subject/Context pairing.

<a id="authority-envelope"></a>

## 6. Authority Envelope

```yaml
authority_envelope:
  grants:
    - authority_ref: "urn:acme:authority:claims.read"
    - authority_ref: "urn:acme:authority:customer-communication.send"
      human_authorization:
        required: true
      policy_refs:
        - "urn:acme:policy:customer-send"
```

### 6.1 Grant semantics

- An authority\_ref MUST identify durable governance semantics; it MUST NOT merely identify the current vendor capability.

- An authority absent from the effective Authority Envelope is NOT\_GRANTED\_BY\_ENVELOPE.

- NOT\_GRANTED\_BY\_ENVELOPE MUST NOT be interpreted as an explicit deny.

- A referenced policy MAY further constrain a grant; OARS Core does not evaluate that policy.

### 6.2 Human authorization

- human\_authorization.required=true means the grant is subject to qualifying human authorization.

- Proof that authorization occurred is external runtime evidence.

- A Consumer MUST NOT infer that human authorization occurred merely because the grant permits it.

### 6.3 Delegation

```yaml
delegation:
  permitted: true
  delegate_refs:
    - "urn:acme:agent:document-summarizer"
  redelegation: false
```

Draft 0.4 does not define grant-level delegation or transitive delegation semantics. Consumers **MUST NOT** infer them.

<a id="assessment"></a>

## 7. Assessment

```yaml
assessment:
  decision: "approved"
  effective:
    from: "2027-01-01T09:00:00Z"
    until: "2027-12-31T23:59:59Z"
  references:
    - rel: "assessment_evidence"
      type: "oscal"
      ref: "urn:acme:oscal:assessment:claims-2027"
```

- A Producer representing an effective approved governance state MUST include an Assessment decision.

- Detailed assessment activities, findings, risks, and evidence SHOULD be referenced rather than duplicated.

- Expiration of an Assessment does not itself define enforcement behavior; that behavior belongs to external policy/enforcement systems.

<a id="bindings"></a>

## 8. Bindings

### 8.1 Subject Binding

```yaml
subject_binding:
  scope_ref: "urn:acme:oars:scope:claims-eu-production"
  implementation:
    type: "aws_agent"
    ref: "AG-441"
  asserted_by: "urn:acme:platform-governance"
  effective:
    from: "2027-07-01T00:00:00Z"
```

- A Subject Binding MUST identify a Governance Scope, technical target, and effective start.

- A Subject Binding MUST NOT be interpreted as an identity alias assertion.

### 8.2 Authority Binding

```yaml
authority_binding:
  scope_ref: "urn:acme:oars:scope:claims-eu-production"
  authority_ref: "urn:acme:authority:customer-communication.send"
  target:
    type: "a2a_skill"
    ref: "https://agent.example/card#send-customer-message"
  asserted_by: "urn:acme:ai-governance"
  effective:
    from: "2027-07-01T00:00:00Z"
```

- An Authority Binding MUST identify an authority\_ref, technical target, and effective start.

- Capability discovery MUST NOT by itself create an Authority Binding.

- A governance-significant binding SHOULD identify its asserter and supporting evidence.

### 8.3 Runtime correlation

```yaml
oars.subject.id
oars.context.id
```

Profiles **MAY** propagate these identifiers. They are correlation claims, not proof of identity or Context.

<a id="temporal-and-record-model"></a>

## 9. Temporal and Record Model

- Issued time and effective time MUST remain distinguishable.

- A Consumer evaluating historical behavior MUST resolve records and bindings effective at the relevant evaluation time.

- A correction MUST NOT silently erase the existence of the corrected record.

| Element | Meaning |
| --- | --- |
| issued\_at | When the OARS statement was issued. |
| effective.from | When represented governance state begins. |
| effective.until | When it ceases, if known. |
| supersedes | Later record represents a genuine governance-state change. |
| corrects | Later record corrects an error in an earlier representation. |

<a id="serialization"></a>

## 10. Serialization

Draft 0.4 defines JSON as the first machine-readable serialization for interoperability testing. YAML examples in this document are presentation equivalents. The accompanying JSON Schema is experimental and is not yet a stable 1.0 wire contract.

- JSON property names are case-sensitive.

- Timestamps MUST use RFC 3339 date-time syntax.

- Implementations MUST preserve unknown extension content when acting as pass-through processors if preservation is technically feasible.

- Core extension data SHOULD be placed under extensions or a profile-defined namespace to reduce collision risk.

The [Core JSON Schema](../schema/README.md) defines the experimental machine-readable representation for this draft.

<a id="processing-model"></a>

## 11. Processing Model

This section is normative. It defines the minimum deterministic behavior of an OARS Core Consumer for authority resolution.

### 11.1 Inputs

The authority-resolution operation accepts: Subject identifier S, Context identifier C, Authority identifier A, and evaluation time T.

### 11.2 Resolution algorithm

1. Resolve the Governance Scope whose Subject identifier equals S and Context identifier equals C. If no scope can be resolved, return UNKNOWN\_SCOPE.

2. Select records for that Governance Scope whose effective period contains T.

3. Apply record-history semantics: a valid correction applicable to the same historical state takes precedence over the corrected representation; a superseding record applies only according to its own effective period.

4. From the remaining applicable record set, resolve the Authority Envelope effective at T. If no unambiguous envelope can be resolved, return INDETERMINATE.

5. Search grants for authority\_ref equal to A. If no grant exists, return NOT\_GRANTED\_BY\_ENVELOPE.

6. If a matching grant exists and human\_authorization.required=true, return GRANTED\_SUBJECT\_TO\_HUMAN\_AUTHORIZATION.

7. If a matching grant contains one or more policy\_refs, return GRANTED\_SUBJECT\_TO\_POLICY unless a more specific result in Step 6 applies; a Consumer MAY report both constraints.

8. Otherwise return GRANTED.

9. When correlating observed implementation behavior, resolve Subject Bindings and Authority Bindings whose effective periods contain T. Binding resolution does not change the result of Steps 1-8; it establishes the implementation mapping used to interpret evidence.

### 11.3 Resolution result vocabulary

| Result | Meaning |
| --- | --- |
| GRANTED | Authority A is present without an OARS Core human-authorization or policy-reference constraint. |
| GRANTED\_SUBJECT\_TO\_HUMAN\_AUTHORIZATION | Authority A is present and requires qualifying human authorization. |
| GRANTED\_SUBJECT\_TO\_POLICY | Authority A is present and references external policy constraints. |
| NOT\_GRANTED\_BY\_ENVELOPE | Authority A is absent from the effective envelope; this is not an explicit deny. |
| UNKNOWN\_SCOPE | No Governance Scope for S x C can be resolved. |
| INDETERMINATE | Applicable OARS state cannot be resolved unambiguously. |

Repository execution conventions and unresolved edge cases are explicitly separated in [DECISIONS.md](../docs/DECISIONS.md). These conventions are separate from the Core processing requirements. The steps above are applied in their listed order.

<a id="conformance"></a>

## 12. Conformance

Conformance claims apply to defined conformance targets. Each claim **MUST** identify the exact OARS Core version.

### 12.1 Conformance targets

| Target | Functional definition |
| --- | --- |
| Core Producer | Emits OARS Core records. |
| Core Consumer | Parses OARS Core records and implements the Section 11 processing model. |
| Binding Producer | Emits Subject Bindings and/or Authority Bindings. |
| Profile Implementation | Implements a named OARS profile in addition to any declared Core class. |

### 12.2 CC-PRODUCER: Core Producer

A Core Producer conforms to Draft 0.4 if it satisfies all **MUST**-level requirements in Sections 2, 5-7, 9-10 applicable to Producers and emits records valid against the Draft 0.4 Core schema.

### 12.3 CC-CONSUMER: Core Consumer

A Core Consumer conforms to Draft 0.4 if it satisfies all **MUST**-level requirements applicable to Consumers and implements the resolution behavior in Section 11.

### 12.4 CC-BINDING: Binding Producer

A Binding Producer conforms to Draft 0.4 if it satisfies all **MUST**-level requirements in Section 8 applicable to the binding types it emits.

### 12.5 Conformance claim format

```yaml
OARS-Core: 0.4-draft
Conformance-Class:
  - Core-Consumer
Supported-Profiles:
  - OARS-OpenTelemetry/0.1-draft
```



<a id="extensibility-and-profiles"></a>

## 13. Extensibility and Profiles

- A Profile MUST NOT redefine the meaning of a Core object or Core resolution result.

- A Profile MAY add fields, binding target types, reference relationships, or processing needed to map another ecosystem into OARS.

- A Core Consumer SHOULD ignore unknown optional extension fields it does not understand and SHOULD preserve them when re-emitting records.

- An extension that changes the meaning of a Core field is a breaking Core change, not an extension.

<a id="versioning-and-compatibility"></a>

## 14. Versioning and Compatibility

- Every Core artifact MUST declare oars\_version.

- A conformance claim MUST declare the exact Core version.

- Profiles MUST version independently from OARS Core.

- Before 1.0, breaking changes MAY occur and MUST be documented in the History appendix.

| Change | Draft 0.x classification | 1.x intended classification |
| --- | --- | --- |
| Add optional field | Normally non-breaking | Non-breaking |
| Add optional profile | Non-breaking | Non-breaking |
| Add new binding target type | Normally non-breaking | Non-breaking if old consumers can ignore it |
| Change existing field meaning | Breaking | Breaking; requires major version |
| Remove/rename field | Breaking | Breaking; requires major version |
| Change Section 11 resolution semantics | Breaking | Breaking; requires major version |
| Tighten optional requirement to mandatory | Potentially breaking | Breaking unless introduced by a new conformance profile |

<a id="security-considerations"></a>

## 15. Security Considerations

- An OARS record is a governance statement, not proof that enforcement occurred.

- A Subject Binding or Authority Binding may be false, stale, or malicious; high-assurance consumers require a trust basis.

- Self-declared capability metadata MUST NOT automatically become enterprise authority.

- Runtime correlation attributes may be spoofed unless established by trusted infrastructure.

- Referenced artifacts may change or disappear; high-assurance deployments SHOULD preserve immutable references, digests, signatures, or archival copies using external mechanisms.

- Consumers SHOULD detect overlapping effective records or bindings that create ambiguous resolution and return INDETERMINATE rather than silently choosing one.

<a id="privacy-considerations"></a>

## 16. Privacy Considerations

- OARS records can reveal organizational structure, business purpose, authority boundaries, and sensitive control design.

- Context identifiers SHOULD avoid embedding unnecessary personal data or secrets.

- References to runtime evidence SHOULD minimize disclosure and SHOULD use access-controlled indirection where the evidence contains prompts, customer data, or other sensitive content.

- Implementations SHOULD apply data minimization and access controls appropriate to the sensitivity of governance metadata.

<a id="registry-and-iana-considerations"></a>

## 17. Registry and IANA Considerations

Draft 0.4 requires no IANA actions. OARS may eventually maintain project registries for profile identifiers, binding target types, reference relationship types, and common authority namespaces. Until governance for such registries is established, implementations **SHOULD** use collision-resistant, organization-controlled identifiers and **MUST NOT** assume an unregistered short name is globally unique.

<a id="canonical-portability-example"></a>

## 18. Canonical Portability Example

Acme operates Claims Assistant in EU production. It is implemented first on a Microsoft-based agent platform and later on AWS. The example is non-normative; vendor names are illustrative.

At cutover, Microsoft Subject and Authority Bindings end and AWS bindings begin. The Subject, Context, accountability, enterprise authority identifiers, and Authority Envelope remain stable unless governance meaning changes. Late evidence from the Microsoft period is evaluated against the historical record and bindings effective at the evidence evaluation time, not against current AWS state.

| Stable semantic | Period A | Period B |
| --- | --- | --- |
| Subject | Claims Assistant | Claims Assistant |
| Context | Claims EU Production | Claims EU Production |
| Authority: communication.send | Microsoft send skill | AWS dispatch capability |
| Human authorization | Required | Required |
| Implementation | MS-817 | AG-441 |
| Enterprise authority ID | Unchanged | Unchanged |

<a id="implementation-considerations"></a>

## 19. Implementation Considerations

- A storage implementation may use relational, graph, document, object, or version-control storage; OARS does not mandate persistence technology.

- Indexes on Subject, Context, Authority, and effective period are recommended for deterministic historical resolution.

- Implementations should retain source-system identifiers as binding targets rather than canonicalizing them into the Subject ID.

- A conformance test suite should include migration, late evidence, retrospective correction, overlapping records, multi-context reuse, and untrusted binding cases.

<a id="normative-references"></a>

## 20. Normative References

[RFC2119] Bradner, S., Key words for use in RFCs to Indicate Requirement Levels, BCP 14, RFC 2119.

[RFC8174] Leiba, B., Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words, BCP 14, RFC 8174.

[RFC3339] Klyne, G. and C. Newman, Date and Time on the Internet: Timestamps, RFC 3339.

[JSON] Bray, T., The JavaScript Object Notation (JSON) Data Interchange Format, RFC 8259.

[JSON-SCHEMA] JSON Schema, Draft 2020-12.

<a id="informative-references"></a>

## 21. Informative References

[A2A] Agent2Agent Protocol Specification, current public specification.

[OASF] AGNTCY Open Agentic Schema Framework and Agent Record documentation.

[MCP] Model Context Protocol public specification and tool metadata documentation.

[OTEL] OpenTelemetry Specification and GenAI semantic conventions.

[OSCAL] NIST OSCAL Assessment Results Model.

[CYCLONEDX] OWASP CycloneDX Machine Learning Bill of Materials.

[SPDX] SPDX 3 AI Profile.

[OASIS-CONFORMANCE] OASIS Guidelines to Writing Conformance Clauses.

<a id="appendix-a-complete-example-record"></a>

## Appendix A. Complete Example Record

```json
{
  "oars_version": "0.4-draft",
  "record": {
    "id": "urn:acme:oars:record:claims:002",
    "issued_at": "2027-03-01T00:00:00Z",
    "issued_by": "urn:acme:ai-governance",
    "relationship": {
      "type": "supersedes",
      "ref": "urn:acme:oars:record:claims:001"
    }
  },
  "scope": {
    "id": "urn:acme:oars:scope:claims-eu-production",
    "subject": {
      "id": "urn:acme:ai-system:claims-assistant",
      "type": "ai_system"
    },
    "context": {
      "id": "urn:acme:context:claims-eu-production",
      "purpose_ref": "urn:acme:use-case:claims-assistance"
    }
  },
  "accountability": [
    {
      "role": "accountable",
      "party_ref": "urn:acme:org:claims"
    }
  ],
  "effective": {
    "from": "2027-03-01T00:00:00Z"
  },
  "authority_envelope": {
    "grants": [
      {
        "authority_ref": "urn:acme:authority:claims.read"
      },
      {
        "authority_ref": "urn:acme:authority:customer-communication.draft"
      },
      {
        "authority_ref": "urn:acme:authority:customer-communication.send",
        "policy_refs": [
          "urn:acme:policy:low-risk-autonomous-send"
        ]
      }
    ],
    "delegation": {
      "permitted": true,
      "delegate_refs": [
        "urn:acme:agent:document-summarizer"
      ],
      "redelegation": false
    }
  },
  "assessment": {
    "decision": "approved",
    "references": [
      {
        "rel": "assessment_evidence",
        "type": "oscal",
        "ref": "urn:acme:oscal:assessment:claims-2027"
      }
    ]
  }
}
```

<a id="appendix-b-design-rationale-non-normative"></a>

## Appendix B. Design Rationale (Non-Normative)

OARS deliberately places stable enterprise semantics above vendor implementation. Capability discovery standards can say what an agent or tool advertises; OARS records what enterprise governance has granted. This separation is the mechanism that allows governance meaning to survive platform migration.

The Core remains intentionally narrow. Policy languages, telemetry, assessment evidence, identity trust, and composition standards are referenced because duplicating them would increase schema breadth without improving governance portability.

<a id="appendix-c-acknowledgements"></a>

## Appendix C. Acknowledgements

Acknowledgements will be added as public reviewers and implementation contributors participate in the OARS process.

<a id="appendix-d-history"></a>

## Appendix D. History

| Draft | Major changes |
| --- | --- |
| 0.4 | Added standards-grade structure, terminology, JSON serialization, deterministic processing model, conformance targets/clauses, versioning, privacy, registry considerations, and release artifacts. |
| 0.3 | Public-review framing, adjacent-standards positioning, security/trust considerations, canonical portability example. |
| 0.2 | Narrowed OARS from a broad agent registry to Governance Scope, Authority Envelope, Assessment, Subject Binding, and Authority Binding. |

<a id="repository-examples"></a>

## Appendix E. Repository examples and implementation guidance

- [Claims Assistant](0001-oars-core/claims-assistant.json) is the complete record from Appendix A. Its predecessor is external to that single-record example.
- [Migration from Microsoft to AWS](0001-oars-core/migration-microsoft-aws.json) keeps Subject, Context, Assessment, accountability, and the Authority Envelope unchanged. Microsoft mappings end when AWS mappings start. Human authorization remains required across the cutover. Vendor names and Acme identifiers are illustrative.
- [Retrospective correction](0001-oars-core/retrospective-correction.json) retains the erroneous original statement and a later-issued correction covering the same effective state. The change corrects representation, rather than purporting to grant new authority in the past.

The portability acceptance criterion is that a neutral consumer can reconstruct authority, context, assessment, and implementation mappings at a relevant time without requiring the historical vendor’s proprietary governance model.

The latter two files are fixture containers with `records` and optional binding arrays. They do not define a standardized batch wire format. [Conformance documentation](../conformance/README.md) explains schema and semantic validation and expected failures. The [Python harness](../reference/python/README.md) exercises deterministic results; [TypeScript](../reference/typescript/README.md) is an implementation scaffold.

Effective time selects historical governance state. Issued time records when the statement was made. The Core history model does not use newest-issued-wins. External policy references and human authorization constraints do not establish that policy passed or authorization occurred. Do not collapse missing grants into deny, and do not treat technical capability or a binding as a grant.

### Repository edition history

- 2026-10-07: Publish the Core project RFC with experimental JSON Schemas, migration and correction examples, conformance cases, and a Python reference harness. The Core version remains `0.4-draft`; open serialization and resolution questions are documented in the decision log.

### Reference links

- [BCP 14: RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).
- [RFC 3339 timestamps](https://www.rfc-editor.org/rfc/rfc3339) and [RFC 8259 JSON](https://www.rfc-editor.org/rfc/rfc8259).
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12).
- [Harbor ATIF project RFC](https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md): publication-structure inspiration only; no Harbor data model or governance is adopted.

The informative ecosystems named in Section 21 are context, not a claim that profiles, integrations, or current-version compatibility have been implemented.
