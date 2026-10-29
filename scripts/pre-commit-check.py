#!/usr/bin/env python3
"""Pre-commit gate: build the site and fail the commit on broken links.

This catches the exact class of bugs that shipped before: 45 dead internal
links, 22 `href="None..."` targets and 153 `<a>` tags without an href.

Usage:
    python scripts/pre-commit-check.py            # build + full check
    python scripts/pre-commit-check.py --no-build # check the existing dist/
"""
import os
import subprocess
import sys

PY = sys.executable


def sh(args, **kw):
    print('$ %s' % ' '.join(args))
    p = subprocess.run(args, **kw)
    return p.returncode


def main():
    skip_build = '--no-build' in sys.argv

    if not skip_build:
        npm = 'npm.cmd' if os.name == 'nt' else 'npm'
        rc = sh([npm, 'run', 'build'])
        if rc != 0:
            print('\nBUILD FAILED - commit aborted')
            return rc

    failures = []
    for script, label in [
        ('scripts/scan-all-404.py', 'internal link check'),
        ('scripts/verify-no-empty-a.py', 'empty <a> check'),
    ]:
        rc = sh([PY, script])
        if rc != 0:
            failures.append(label)

    # informational only - never blocks the commit
    sh([PY, 'scripts/audit-data-gaps.py'])

    if failures:
        print('\nPRE-COMMIT CHECK FAILED: %s' % ', '.join(failures))
        print('Commit aborted. Fix the issues above (or use --no-verify to bypass).')
        return 1

    print('\nPRE-COMMIT CHECK PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main())
