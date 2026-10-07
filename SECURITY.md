# Security and reporting

This draft and its experimental harness are not an enforcement engine, identity provider, policy evaluator, or attestation system. No supported production releases or response service levels are declared.

Report vulnerabilities through [GitHub's private vulnerability reporting](https://github.com/catalinnovac03/oars/security/advisories/new). Private reporting is enabled for this repository. Include the affected version, impact, reproduction, and a minimal synthetic record. Do not post exploitable details, secrets, customer records, or private evidence in public issues.

Named security contacts and response commitments remain unassigned.

Schema validity does not establish issuer authority or trustworthy bindings. Verify provenance, authorization to assert records, integrity, reference immutability, and trust outside Core. Treat imported identifiers and references as untrusted; do not automatically dereference URLs. Apply access controls and minimize sensitive context and evidence. See [RFC security and privacy](rfcs/0001-oars-core.md#security-considerations).

The harness uses fixture trust labels only to exercise binding scenarios. It performs no cryptographic verification and must not be used to authorize runtime actions.
