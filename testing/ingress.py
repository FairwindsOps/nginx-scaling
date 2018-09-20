#!/usr/bin/env python2

import json
import uuid
import os.path
from kubernetes import client, config
import yaml
import requests
from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue
from reload_time import check_nginx_reload

NS = "ingress-testing"
baseurl = "test.sudermanjr.hillghost.com"

def generate_new_hosts_list(ingress_count):
    """Write the hosts file if it does not exist"""
    if not os.path.isfile("hosts.txt"):
        with open("hosts.txt", "w") as file:
            for _ in range(ingress_count):
                file.write("{}.{}\n".format(uuid.uuid4(), baseurl))

def batch(iterable, batchSize):
    l = len(iterable)
    for ndx in range(0, l, batchSize):
        yield iterable[ndx:min(ndx + batchSize, l)]

def load_hosts_list():
    """grab the list of hosts"""
    with open('hosts.txt', 'r') as f:
        hosts = f.read().splitlines()
    return hosts

def update_ingresses(ingress_count, batchSize):
    """
    Generates the necessary hostnames and then applies the ingress
    If the number increases, don't change the names, just append to them.
    """
    # Do an initial generation of the file
    generate_new_hosts_list(ingress_count)

    # If the new number is different than the existing, then delete the hosts.txt and then regenerate it.
    if len(load_hosts_list()) != ingress_count:
        os.remove("hosts.txt")
        generate_new_hosts_list(ingress_count)

    # Append more entries if you need them
    length = len(load_hosts_list())
    if length < ingress_count:
        with open('hosts.txt', 'a') as f:
            for _ in range(ingress_count - length):
                f.write("{}.{}\n".format(uuid.uuid4(), baseurl))

    # Read the hosts into the list again
    hosts = load_hosts_list()

    ingressCount = 1
    for hostBatch in batch(hosts, batchSize):
        ingress_header = """
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-{}
  annotations:
    kubernetes.io/ingress.class: "nginx-ingress"
spec:
  rules:""".format(ingressCount)

        # Create the ingress definition
        with open("ingresses/test-{}.yaml".format(ingressCount), "w") as file:
            file.write(ingress_header)

            for host in hostBatch:
                ingress_host = """
    - host: {}
      http:
        paths:
        - backend:
            serviceName: test-service
            servicePort: 80
          path: /""".format(host)

                file.write(ingress_host)

        # Deploy the ingress
        with open('ingresses/test-{}.yaml'.format(ingressCount), 'r') as file:
            ing = yaml.load(file)
            k8s_beta = client.ExtensionsV1beta1Api()
            resp = k8s_beta.list_namespaced_ingress(
                namespace=NS)
            exists = False
            for ingress in resp.items:
                if ingress.metadata.name == 'test-{}'.format(ingressCount):
                    exists = True

        if exists:
            resp2 = k8s_beta.replace_namespaced_ingress(body=ing, namespace=NS, name='test-{}'.format(ingressCount))
        else:
            resp2 = k8s_beta.create_namespaced_ingress(body=ing, namespace=NS)

        ingressCount += 1

if __name__ == "__main__":
    update_ingresses(4000, 80)
