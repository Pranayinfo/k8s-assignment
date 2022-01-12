# Docker Compose to Kubernetes Manifests

This is a Basic example of a Docker Compose Deployment.
Consisting of 4 services, with env variables for each service as defined in the file.

## Task

Convert the Given Docker Compose file to a Kubernetes Deployment on GKE Standard.

Ensure a persistent storage solution for postgres data, every other service can be stateless.

Attach a Kubernetes HPA to the backend service to scale the number of replicas.
(Min- 2 replicas, Max- 5 replicas), based on the CPU usage. every other service can have a fixed number of replicas.

The Env variables for PGADMIN service must be passed using kubernetes secrets, every other service can take env variables from configmap

The Frontend and PGADMIN service must be exposed to the outside world, whereas the Backend and postgres need to be internal to the cluster.

Dockerfiles for backend and frontend can be found in their respective folders, feel free to make any changes to the Dockerfiles or the code in the event of failure due to improper code.
