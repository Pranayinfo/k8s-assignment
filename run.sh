# minikube start

docker build -t ps-frontend-image ./frontend/.

docker build -t ps-backend-image ./backend/.

cd k8s/

kubectl apply -f altair-networkpolicy.yaml,pgadmin-data-persistentvolumeclaim.yaml,backend-data-persistentvolumeclaim.yaml,pgadmin-deployment.yaml,backend-deployment.yaml,pgadmin-service.yaml,backend-service.yaml,postgres-data-persistentvolumeclaim.yaml,frontend-data-persistentvolumeclaim.yaml,postgres-deployment.yaml,frontend-deployment.yaml,postgres-service.yaml,frontend-service.yaml 

cd ../

echo "\n Services Applied"

echo "\n backend service running at:"
minikube service backend-service --url

echo "\n frontend service running at:"
minikube service frontend-service --url

echo "\n postgres service running at:"
minikube service postgres-service --url

echo "\n pgadmin service running at:"
minikube service pgadmin --url