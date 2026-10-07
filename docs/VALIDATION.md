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
| Local Markdown and archived HTML links/fragments | 174 passed |
| Archived draft snapshot | SHA-256 matches the archive record |

Run `python tools/validate.py` after installing the requirements in `reference/python/requirements.txt`. The script checks JSON syntax, schemas, fixtures, resolution results, the archived draft checksum, and local links.

The downloadable ZIP uses a single `oars/` root and includes the committed project files. Local `work/` and `outputs/`, caches, virtual environments, Git metadata, and credentials are excluded. Archive entries and bytes are checked against the Git tree before delivery.

GitHub Actions runs the same validation on Python 3.10 and 3.14 for main-branch pushes and pull requests. Action dependencies are pinned to verified official commit IDs. The remote run result is available from the workflow badge in the project README.

## Limits

The JSON serialization and reference-harness conventions are experimental. Compatibility with other draft schema artifacts has not been established. Semantic checks do not validate real issuer authority, signatures, external policy, human approval evidence, all RFC 3339 edge cases, or every prose requirement. External web links are not part of the local-link test. TypeScript and profiles are documented scaffolds, not implemented integrations. No license or governance identity has been assigned.
