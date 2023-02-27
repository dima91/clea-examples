
#!/bin/bash

cd $(dirname $0)

source venv/bin/activate
python3 tests/vendtrace_tester.py -c config.ini