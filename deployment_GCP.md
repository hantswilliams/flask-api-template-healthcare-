# Deployment with GCP with Dockerfile.Prod

## Setup with MySQL DB
- Recommend using a cloud environment of you choosing (e.g., GCP, AWS, Azure) to deploy a managed MySQL DB instance
- Create that instance, and then update the .ENV file with the appropriate credentials so that the app can connect to the DB
- The run commands will be the same as the local setup, but the app will be connecting to the cloud DB instance when you deploy in the following steps using Docker

## Utilization Cloud Run
- Prequests:
    - Need to push image to a registry, like docker hub 
        - e.g., `docker buildx build --platform linux/amd64 -f Dockerfile.Prod -t flaskhealth .` # this is important for building on a M1/M2 processor, also makes it easier to run on cloud based services that will be running a linux varient  
            - or with custom named Dockerfile.Prod:
                - e.g., `docker buildx build --platform linux/amd64 -f Dockerfile.Prod -t flaskhealth .`
        - e.g., `docker tag flaskhealth hants/flaskhealth:V0.0.X`
        - e.g., `docker push hants/flaskhealth:V0.0.X`
    - In the current iteration, have pushed image to docker hub (docker.io/hants/flaskhealth)

- Steps:
    - Create a new service in Cloud Run
    - Select the image from the registry
    - **Note**: the image needs to be public, and make sure the `.ENV` file is also replicated into the test_app folder
    - Set the port in the image to match the port in the Cloud Run service, which currently is 5001