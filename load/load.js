import http from "k6/http";
import { check, fail } from "k6";
import { Rate } from "k6/metrics";

export let errorRate = new Rate("errors");
export let options = {
  stages: [
    { duration: "5m", target: 1 },
    { duration: "60m", target: 1 },
    { duration: "5m", target: 0 },
  ]
};

let hostnameFile = open("./hosts.txt");
let hostnames = hostnameFile.split("\n")

export default function() {
    var i;
    for (i = 0; i < hostnames.length; i++) {

        let res = http.get("http://" + hostnames[i]);

        check(res, {
            "is status 200": (r) => r.status === 200
        });
        errorRate.add(res.status != 200);
    }
};
