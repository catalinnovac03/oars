# Validation report

Validated on 2026-10-07 using Python 3.14 and jsonschema 4.26.0 with date-time format checking enabled.

| Check | Result |
|---|---|
| Strict JSON syntax, including duplicate-key/non-finite-value rejection | 49 documents passed |
| Draft 2020-12 schema metaschema checks | 3 schemas passed |
| Valid records, binding documents, scenario files, and nested records/bindings | 36 positive documents passed |
| Intentionally invalid records | 9 failed at their documented layer, path, and rule |
| Authority-resolution cases | 27 passed |
| Complete record/binding order permutations | 65 passed; no input mutation |
| JSON examples embedded in the RFC | 2 parsed and schema-validated |
| Local Markdown and source HTML links/fragments | 173 passed |
| Source snapshot | SHA-256 matches the provenance record |
| Source normative paragraph preservation | All 47 source paragraphs containing MUST, SHOULD, MAY, or REQUIRED retained, with the necessary section-number update |
| Source Appendix A example | Exact equality as a parsed JSON value |

Run `python tools/validate.py` after installing the requirements in `reference/python/requirements.txt`. The script performs the repeatable JSON, schema, fixture, resolution, source-checksum, and link checks. The normative-paragraph and Appendix A comparisons were also performed against the uploaded HTML during assembly.

The downloadable ZIP uses a single `oars/` root and includes the committed project files. Local `work/` and `outputs/`, caches, virtual environments, Git metadata, and credentials are excluded. Archive entries and bytes are checked against the Git tree before delivery.

GitHub Actions runs the same validation on Python 3.10 and 3.14 for main-branch pushes and pull requests. Action dependencies are pinned to verified official commit IDs. The remote run result is available from the workflow badge in the project README.

## Limits

The original separately referenced schema was not supplied, so compatibility with that artifact is unverified. The reconstructed schema and resolution conventions are explicitly experimental. Semantic checks do not validate real issuer authority, signatures, external policy, human approval evidence, all RFC 3339 edge cases, or every prose requirement. External web links are not part of the local-link test. TypeScript and profiles are documented scaffolds, not implemented integrations. No license or governance identity has been assigned.
