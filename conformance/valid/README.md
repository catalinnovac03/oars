# Valid fixtures

`core-*.json` validate against the Core schema. `binding-*.json` validate against the binding wrapper schema. The minimal record deliberately has an empty Assessment object: it does not claim an approved governance state. An approved-state producer must include a decision.

`core-source-example.json` reproduces source Appendix A, including its reference to a predecessor that is not embedded in that single record. Structural validation does not imply the history is complete. `core-extensions.json` includes both namespaced extensions and an unknown optional field to exercise the source's extensibility approach.
