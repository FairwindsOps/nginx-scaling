bash -c ./export_hostnames.sh
rm output.json
docker rm -f loadtest
docker run -itd --name loadtest  \
    -v $PWD:/data \
    --env-file $(pwd)/testenv \
    loadimpact/k6 run \
    --out json=/data/output.json \
    /data/load.js
