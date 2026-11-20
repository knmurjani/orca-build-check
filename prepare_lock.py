"""Normalize only pinned upstream's source-less workspace lock versions."""
import hashlib
import pathlib
import re
import tomllib

root = pathlib.Path('upstream/codex-rs')
lock_path = root / 'Cargo.lock'
original = lock_path.read_bytes()
assert hashlib.sha256(original).hexdigest() == '56e04c89b25a6efa1fa6f1cf02934e92451933c8ebda57a5153207ba9ea9fb9e'
before = tomllib.loads(original.decode())
workspace = tomllib.loads((root / 'Cargo.toml').read_text())
assert workspace['workspace']['package']['version'] == '0.169.0'
local = {}
for manifest in root.rglob('Cargo.toml'):
    package = tomllib.loads(manifest.read_text()).get('package', {})
    if 'name' not in package:
        continue
    version = package.get('version')
    if isinstance(version, dict):
        assert version == {'workspace': True}
        version = workspace['workspace']['package']['version']
    local[package['name']] = version
changed = []
sections = original.decode().split('[[package]]')
for index in range(1, len(sections)):
    package = tomllib.loads('[[package]]' + sections[index])['package'][0]
    if 'source' in package:
        continue
    name = package['name']
    assert name in local
    assert package['version'] == '0.0.0'
    assert local[name] == '0.169.0'
    sections[index], count = re.subn(r'(?m)^version = "0\.0\.0"$', 'version = "0.169.0"', sections[index])
    assert count == 1
    changed.append(name)
assert len(changed) == 173 and len(set(changed)) == 173
corrected = '[[package]]'.join(sections).encode()
after = tomllib.loads(corrected.decode())
assert len(before['package']) == len(after['package'])
for old, new in zip(before['package'], after['package']):
    expected = dict(old)
    if 'source' not in old:
        expected['version'] = '0.169.0'
    assert new == expected
assert {k:v for k,v in before.items() if k != 'package'} == {k:v for k,v in after.items() if k != 'package'}
assert hashlib.sha256(corrected).hexdigest() == '200de438778a44c55d452b8931f5293ec3d7bda66c48717605b202764a4d3f7a'
lock_path.write_bytes(corrected)
print('VERIFIED: 173 workspace version fields only; all external dependency records, sources, versions, checksums and dependency edges unchanged.')
print('Cargo.lock SHA256:', hashlib.sha256(corrected).hexdigest())
