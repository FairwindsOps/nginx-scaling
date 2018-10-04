# Running Nginx Ingress With 4k+ Ingresses

This repo is the culmination of a lot of testing and hacking trying to get the nginx-ingress-controller running thousands of ingresses while reloading smoothly.  There are several folders in here:

## manifests

A basic nginx deployment that can be used as an endpoint that will return 200.  Very very basic

## testing

This is where the python scripts for testing reload times are located.  The `run.py` file allows you to set a number of random ingresses and roll through them while collecting data on reload times.  The results folder has some data I collected.  I will continue to add to this as I tweak more and more settings.

##  load

This folder contains some tooling around loadimpact/k6 that allows for generating a lot of load against the server. It has a kube folder that allows you to deploy it to kube as a deployment.  Scaling that deploy generates more traffic.

The `utility-run.sh` script can be used to analyze the results or put them somewhere else.  It runs inside a utility container that mounts the output of the loadtest.

`load.js` is the test itself.  It uses k6.

## Notes from scaling:

* Dynamic reload is great.  Keep your log levels low.  On nginx logging v=3 I saw each nginx controller consume about 15G of memory.
* Disable ipv6 explicitly in nginx-ingress
* Prometheus metrics are not a great option for Datadog and nginx.  Stick to the native nginx metrics.  Memory consumption of the Datadog container gets very high with this number of ingresses.
* The smallest issue is multiplied exponentially when scaling this large.  Keep your changes small and test thoroughly.
