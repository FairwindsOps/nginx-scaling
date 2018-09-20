apk --update add util-linux
mkdir -p /output
cd /k6
k6 run load.js --out json=/output/$(uuidgen).json
