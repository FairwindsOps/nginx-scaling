#!/usr/bin/env python3

from kubernetes import client, config
config.load_kube_config()
import re
from datetime import datetime, timedelta
from time import sleep
timeformat = r'\d{2}:\d{2}:\d{2}.\d{6}'

v1 = client.CoreV1Api()

def check_nginx_reload(controllerName):
    """ Check to see if nginx has completed it's latest reload """

    ret = v1.list_namespaced_pod(watch=False, namespace="infra")
    pod_names = []
    for i in ret.items:
        if controllerName in i.metadata.name:
            pod_names.append(i.metadata.name)

    complete = False
    reload_times = []
    while not complete:
        start_times = {}
        end_times = {}
        for pod_name in pod_names:
            start_times[pod_name] = []
            end_times[pod_name] = []
            log = v1.read_namespaced_pod_log(name=pod_name, namespace="infra", follow=False)
            for line in log.splitlines():
                if "reload" in line:
                    if 'required' in line:
                        match = re.search(timeformat, line)
                        start_times[pod_name].append(datetime.strptime(match.group(), '%H:%M:%S.%f'))
                    if 'reloaded' in line:
                        match = re.search(timeformat, line)
                        end_times[pod_name].append(datetime.strptime(match.group(), '%H:%M:%S.%f'))

        for pod_name in pod_names:
            if len(start_times[pod_name]) != len(end_times[pod_name]):
                sleep(10)
            elif (len(start_times[pod_name]) == 0 or len(end_times[pod_name]) == 0):
                reload_times.append('No Data')
                complete = True
            else:
                complete = True
                for i  in enumerate(end_times[pod_name]):
                    reload = end_times[pod_name][i] - start_times[pod_name][i]
                    reload_sec = reload.total_seconds()
                    reload_times.append(str(reload_sec))

    return reload_times

if __name__ == "__main__":
    print(check_nginx_reload("nginx-ingress-controller"))

