#!/usr/bin/env python2

from ingress import update_ingresses
from reload_time import check_nginx_reload
import json
from time import sleep
import sys
import os

steps = list(range(4001, 4002, 1))
data = {}

try:
    os.mkdir("ingresses")
except:
    pass

if os.path.isfile('results/results.json'):
    print("ERROR - Ouput file already exists.  Exiting.")
    sys.exit(1)
for step in steps:
    print("Ingress Count: {}".format(step))
    update_ingresses(step, 80)
    sleep(5)
    data[step] = check_nginx_reload("nginx-ingress-controller")[0]
    print("Reload Time: {}".format(data[step]))
    with open('results/results.json', 'w') as file:
        file.write(json.dumps(data, indent=2, sort_keys=True))
