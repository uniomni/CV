"""Run test_flood_database.py multiple times

Start 10 background processes running the test.

UNIX only

Ole Nielsen, RAMP 2006
x9048

"""

import os

for i in range(100):
    os.system('python test_flood_database.py &')
