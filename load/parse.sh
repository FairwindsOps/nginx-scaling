echo "###############################"
echo "#####   Load Test Stats   #####"
echo "###############################"

printf "\nSuccess Rate: "
jq '. | select(.type=="Point" and .metric == "checks") .data.value' $1 | jq -s "add/length*100"

printf "\nRequest Duration (ms)\n"

printf "avg: "
jq '. | select(.type=="Point" and .metric == "http_req_duration" and .data.tags.status >= "200") | .data.value' $1 | jq -s 'add/length'

printf "min: "
jq '. | select(.type=="Point" and .metric == "http_req_duration" and .data.tags.status >= "200") | .data.value' $1 | jq -s min

printf "max: "
jq '. | select(.type=="Point" and .metric == "http_req_duration" and .data.tags.status >= "200") | .data.value' $1 | jq -s max

