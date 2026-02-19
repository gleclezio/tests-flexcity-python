# Activation app

The app is built in python with FastAPI and provides a swagger to interact with the **POST /activation** entrypoint.

There is another endpoint (**PUT /assets**) to update the list of assets. 

## How to run the app

Docker is needed to build an image and run the app. 

In *flexcity-app* directory:

- build docker image: `docker build -t flexcity .`
- run docker image: `docker run -d -p 80:80 --name flexcity_app flexcity`
- Access the app: http://127.0.0.1/docs
  - Click on the */activation* endpoint
  - Then click on *Try it out* and fill the *Request body*. Sample data is already provided
  - Then click on *Execute*


### In dev mode

Python 3.14 and poetry are needed to run the app in dev mode.

In *flexcity-app* directory:

- Setup env with poetry: `poetry env activate` then `poetry install`
- Run the app: `fastapi dev .\src\flexcity_app\main.py`
- Access the app at: http://127.0.0.1:8000/docs
  - Click on the */activation* endpoint
  - Then click on *Try it out* and fill the *Request body*. Sample data is already provided
  - Then click on *Execute*

To be able to build image docker, the app needs to be built first.
- Build the app: `poetry build`

## Assumptions
- each asset volume is > 0 (no check is done)
- In case we are not able to strictly satisfy volume request. The selection of assets will be able to provide more power.
  - In activation output data, each asset will have:
    - a *volume* field which is the max volume that can be activated for this asset
    - a *power_requested* field which is the volume has to be activated for this activation request
- In case activation request volume is > total available volume, a 500 error is returned

## To be improved
- docker image
  - find a better base image to reduce the size of the final image
- Availability date management for asset ?
- Case where we do not have enough asset volume to satisfy demand ?