"""Exact two actual-Rust derivation/optional-output tests. No partial or stale one-test pass."""
import json
from pathlib import Path
import re
import sys
expected = json.loads((Path(__file__).parent / 'expected-conformance-tests.json').read_text())
assert len(expected) == 2 and len(set(expected)) == 2
s = Path(sys.argv[2]).read_text()
if sys.argv[1] == 'list':
    names = re.findall(r'^(.+): (?:test|benchmark)$', s, re.M)
    assert len(names) == 2 and sorted(names) == sorted(expected)
elif sys.argv[1] == 'result':
    results = re.findall(r'^test (.+) \.\.\. (.+)$', s, re.M)
    assert len(results) == 2
    assert sorted(results) == sorted((n, 'ok') for n in expected)
    summaries = re.findall(r'^test result: (.+)$', s, re.M)
    assert len(summaries) == 1
    assert re.fullmatch(r'ok\. 2 passed; 0 failed; 0 ignored; 0 measured; \d+ filtered out; finished in [0-9.]+s', summaries[0])
else:
    raise AssertionError('mode')
print('VERIFIED exact2 conformance tests', sys.argv[1])
