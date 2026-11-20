"""Fail closed if libtest selection or results differ from the frozen 34 tests."""
import hashlib
import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent
expected_bytes = (root / 'expected-tests.json').read_bytes()
assert hashlib.sha256(expected_bytes).hexdigest() == '415bd858f789fd3e0737166242959d28ca8731853630ac0eec3913715d86b0ab'
expected = json.loads(expected_bytes)
assert len(expected) == 34 and len(set(expected)) == 34
text = pathlib.Path(sys.argv[2]).read_text()
if sys.argv[1] == 'list':
    observed = re.findall(r'^(event_processor_with_json_output::\w+): test$', text, re.M)
    assert sorted(observed) == expected
    assert len(re.findall(r'^.+: (?:test|benchmark)$', text, re.M)) == 34
elif sys.argv[1] == 'result':
    observed = re.findall(r'^test (event_processor_with_json_output::\w+) \.\.\. ok$', text, re.M)
    assert sorted(observed) == expected
    assert len(re.findall(r'^test .+ \.\.\. ', text, re.M)) == 34
    summaries = re.findall(r'^test result: (.+)$', text, re.M)
    assert len(summaries) == 1
    assert re.fullmatch(r'ok\. 34 passed; 0 failed; 0 ignored; 0 measured; \d+ filtered out; finished in [0-9.]+s', summaries[0])
else:
    raise SystemExit('unsupported verification stage')
print('VERIFIED exact 34 selected offline event processor tests:', sys.argv[1])
