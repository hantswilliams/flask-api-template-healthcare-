# Deployment with GCP

## Utilization Cloud Run
- Prequests:
    - Need to push image to a registry, like docker hub 
        - e.g., `docker buildx build --platform linux/amd64 -t flaskhealth .` # this is important for building on a M1/M2 processor 
        - e.g., `docker tag flaskhealth hants/flaskhealth:V00X`
        - e.g., `docker push hants/flaskhealth:V00X`
    - In the current iteration, have pushed image to docker hub (docker.io/hants/flaskhealth)

- Steps:
    - Create a new service in Cloud Run
    - Select the image from the registry
    - **Note**: the image needs to be public, and make sure the `.ENV` file is also replicated into the test_app folder
    - Set the port in the image to match the port in the Cloud Run service, which currently is 5001