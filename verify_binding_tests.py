"""Strict seven new lib-test list/result guard, no native execution."""
import json,pathlib,re,sys
root=pathlib.Path(__file__).resolve().parent
expected=json.loads((root/'expected-binding-tests.json').read_text())
assert len(expected)==7 and len(set(expected))==7
text=pathlib.Path(sys.argv[2]).read_text()
if sys.argv[1]=='list':
    observed=re.findall(r'^(exec_binding_observation::tests::\w+): test$',text,re.M)
    assert len(re.findall(r'^.+: (?:test|benchmark)$',text,re.M))==7
elif sys.argv[1]=='result':
    observed=re.findall(r'^test (exec_binding_observation::tests::\w+) \.\.\. ok$',text,re.M)
    assert len(re.findall(r'^test .+ \.\.\. ',text,re.M))==7
    summaries=re.findall(r'^test result: (.+)$',text,re.M)
    assert len(summaries)==1 and re.fullmatch(r'ok\. 7 passed; 0 failed; 0 ignored; 0 measured; \d+ filtered out; finished in [0-9.]+s',summaries[0])
else:raise SystemExit('stage')
assert sorted(observed)==sorted(expected)
print('VERIFIED exact7 binding observer lib tests',sys.argv[1])
