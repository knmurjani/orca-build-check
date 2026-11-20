"""Guard the one test-only actual Rust derivation export, exact selection and outcome."""
import re
from pathlib import Path
import sys
name = 'exec_schema_conformance_tests::emit_actual_derivations_and_wire_matrix'
s = Path(sys.argv[2]).read_text()
if sys.argv[1] == 'list':
    assert re.findall(r'^(.+): (?:test|benchmark)$', s, re.M) == [name]
elif sys.argv[1] == 'result':
    assert re.findall(r'^test (.+) \.\.\. (.+)$', s, re.M) == [(name, 'ok')]
    summaries = re.findall(r'^test result: (.+)$', s, re.M)
    assert len(summaries) == 1
    assert re.fullmatch(r'ok\. 1 passed; 0 failed; 0 ignored; 0 measured; \d+ filtered out; finished in [0-9.]+s', summaries[0])
else:
    raise AssertionError('mode')
print('VERIFIED exact1 conformance test', sys.argv[1])
