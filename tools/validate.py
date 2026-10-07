#!/usr/bin/env python3
"""Run all repository checks without network access or rewriting any file."""
import copy
import hashlib
from html.parser import HTMLParser
import itertools
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'reference/python'))
from resolver import resolve, correlate, semantic_errors


def repository_files(suffix):
    """Exclude local generated files and environments from repository checks."""
    excluded = {'work', 'outputs', '.git', '.venv', 'node_modules', '__pycache__'}
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [name for name in subdirectories if name not in excluded]
        for name in filenames:
            if name.endswith(suffix):
                yield Path(directory) / name


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('Duplicate JSON property: ' + key)
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError('Non-JSON constant: ' + value)


def load(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def pointer(parts):
    return '/' + '/'.join(str(x).replace('~', '~0').replace('/', '~1') for x in parts)


def anchors(path):
    text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+)$', text, flags=re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(slug + ('-' + str(count) if count else ''))
    return result


def main():
    docs = {p: load(p) for p in repository_files('.json')}
    schemas = {p.name: doc for p, doc in docs.items() if p.parent == ROOT / 'schema'}
    base_uri = (ROOT / 'schema').as_uri() + '/'
    registry = Registry().with_resources((base_uri + name, Resource.from_contents(doc))
                                         for name, doc in schemas.items())
    validators = {}
    for name, schema in schemas.items():
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(
            {'$ref': base_uri + name}, registry=registry, format_checker=FormatChecker())
    validated = 0
    for path, doc in docs.items():
        relative = path.relative_to(ROOT).as_posix()
        kind = None
        if relative.startswith('conformance/valid/'):
            kind = 'oars-binding.schema.json' if path.name.startswith('binding-') else 'oars-core.schema.json'
        elif relative == 'rfcs/0001-oars-core/claims-assistant.json':
            kind = 'oars-core.schema.json'
        elif relative.startswith('rfcs/0001-oars-core/') or relative.startswith('conformance/resolution-cases/'):
            kind = 'fixture.schema.json'
        if kind:
            validators[kind].validate(doc)
            validated += 1
    manifest = load(ROOT / 'conformance/invalid/manifest.json')
    listed = {c['file'] for c in manifest['cases']}
    actual = {p.name for p in (ROOT / 'conformance/invalid').glob('*.json') if p.name != 'manifest.json'}
    assert listed == actual, 'Invalid fixture manifest coverage mismatch'
    for case in manifest['cases']:
        doc = load(ROOT / 'conformance/invalid' / case['file'])
        errors = list(validators['oars-core.schema.json'].iter_errors(doc))
        if case['layer'] == 'schema':
            assert any(pointer(e.absolute_path) == case['path'] and e.validator == case['rule']
                       for e in errors), (case, [str(e) for e in errors])
        else:
            assert not errors, (case, errors)
            assert (case['path'], case['rule']) in semantic_errors(doc), case
    permutations = 0
    cases = sorted((ROOT / 'conformance/resolution-cases').glob('*.json'))
    for path in cases:
        case = load(path)
        original = copy.deepcopy(case)
        for records in itertools.permutations(case['records']):
            for subjects in itertools.permutations(case.get('subject_bindings', [])):
                for authorities in itertools.permutations(case.get('authority_bindings', [])):
                    test = {**case, 'records': list(records), 'subject_bindings': list(subjects),
                            'authority_bindings': list(authorities)}
                    result = resolve(test)
                    assert result['result'] == case['expected']['result'], (path.name, result)
                    if 'expected_constraints' in case:
                        assert result['constraints'] == case['expected_constraints'], path.name
                    if 'expected_mapping' in case:
                        assert correlate(test) == case['expected_mapping'], (path.name, correlate(test))
                    permutations += 1
        assert original == case, 'Resolver mutated input: ' + path.name
    # All otherwise-valid individual records should pass single-record semantic checks.
    for path in (ROOT / 'conformance/valid').glob('core-*.json'):
        assert not semantic_errors(load(path)), path.name
    embedded_json = 0
    links = 0
    for path in repository_files('.md'):
        for block in re.findall(r'```json\s*\n(.*?)```', path.read_text(), flags=re.S):
            document = json.loads(block, object_pairs_hook=unique_object, parse_constant=reject_constant)
            if 'oars_version' in document and 'record' in document:
                validators['oars-core.schema.json'].validate(document)
            embedded_json += 1
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = urlsplit(dest)
            if target.scheme or target.netloc:
                continue
            local = (path.parent / unquote(target.path)).resolve() if target.path else path
            assert local.is_relative_to(ROOT), ('Link escapes repo', path, dest)
            assert local.exists(), ('Broken link', path, dest)
            if target.fragment and local.suffix == '.md':
                assert unquote(target.fragment) in anchors(local), ('Missing anchor', path, dest)
            links += 1
    class SnapshotParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ids, self.hrefs = set(), []
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'id' in attrs:
                self.ids.add(attrs['id'])
            if tag == 'a' and 'href' in attrs:
                self.hrefs.append(attrs['href'])
    snapshot = ROOT / 'provenance/OARS_0.4_Standards_Grade_Public_Review_Draft.html'
    digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    assert digest in (ROOT / 'provenance/README.md').read_text(), 'Archived draft checksum mismatch'
    html = SnapshotParser()
    html.feed(snapshot.read_text())
    for href in html.hrefs:
        if href.startswith('#'):
            assert href[1:] in html.ids, ('Broken snapshot anchor', href)
            links += 1
    print(f'PASS: {len(docs)} JSON documents parsed strictly; {len(schemas)} schemas checked.')
    print(f'PASS: {validated} positive example/fixture documents validated, including nested records/bindings.')
    print(f'PASS: {len(manifest["cases"])} documented invalid fixtures failed at their expected layer/path/rule.')
    print(f'PASS: {len(cases)} resolution cases; {permutations} complete record/binding permutations; inputs preserved.')
    print(f'PASS: {embedded_json} embedded JSON examples; archived draft checksum; {links} local links/fragments.')


if __name__ == '__main__':
    main()
