currentdir=$(pwd)

kubectl get -n k6-nginx configmap k6files && kubectl delete configmap -n k6-nginx k6files || true
kubectl get -n k6-nginx configmap utilities && kubectl delete configmap -n k6-nginx utilities || true
kubectl create configmap \
    -n k6-nginx k6files \
    --from-file=../load.js \
    --from-file=run.sh \
    --from-file=../../testing/hosts.txt
kubectl create configmap \
    -n k6-nginx utilities \
    --from-file=../parse.sh \
    --from-file=utility-run.sh
kubectl -n k6-nginx apply -f deployment.yaml
