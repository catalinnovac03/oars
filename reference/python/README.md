# Python experimental reference harness

Run from the repository root with Python 3.10 or later:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r reference/python/requirements.txt
.venv/bin/python tools/validate.py
```

[resolver.py](resolver.py) demonstrates the source processing model under the explicit [repository conventions](../../docs/DECISIONS.md). [The validator](../../tools/validate.py) checks JSON syntax, schema structure and instances, documented invalid cases, semantic cases, resolution outputs with all record/binding permutations, and local Markdown links.

This is experimental reference code, not a production SDK or a full Core-Consumer conformance claim. Records must already have been accepted by an external trust process. Binding trust names in test input are synthetic test controls, not proofs. No policies, URLs, credentials, signatures, or enforcement actions are evaluated. The harness accepts ordinary RFC 3339 datetimes with offsets; leap seconds are not supported by Python datetime.

Dependencies are installed locally; no dependency source is bundled. Unknown fields are retained in input objects and never stripped by resolution. Resolution does not modify the input dataset.
