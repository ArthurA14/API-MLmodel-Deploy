# groupe6
By conserving wildlife, we're ensuring that future generations can enjoy our natural world.

![image](https://user-images.githubusercontent.com/57401552/210325880-fd86a618-3812-471a-82f3-6dd79716f01c.png)

### Deliveries :
- Github repository URL with all elements *(code, Dockerfile, workflow configuration Github)* : *https://github.com/efrei-ADDE92-CTP/groupe6*
- Name of the docker image on Azure Container Registry (ACR) : ***`group6-container`***
- Endpoint API on Azure Container App : *https://group6-container.ashycliff-15f451bd.westeurope.azurecontainerapps.io*

---
### 0. Preliminary preparation

````bash
WSL2 :
arthur@DESKTOP-OBTCMJQ:/mnt/c/Windows/system32$

$ cd ../..
arthur@DESKTOP-OBTCMJQ:/mnt/c$

$ cd Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet
arthur@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet$

$ source MYVENV/bin/activate
(MYVENV) arthur@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet$
````

---
### 1. *Python* dependencies to install

````python
$ pip install matplotlib==3.5.3
$ pip install numpy==1.21.6
$ pip install pandas==1.3.5         ou sudo apt-get install python3-pandas
$ pip install scikit-learn==1.0.2
$ pip install starlette             for the web parts
$ pip install pydantic              for the data parts
$ pip install fastapi
$ pip install "uvicorn[standard]"   ASGI server for production
$ pip install -r requirements.txt
$ pip install scipy==1.7.3
$ pip install contourpy==1.0.6
$ pip install prometheus_client
$ sudo apt-get install prometheus
$ pip install starlette
$ pip install starlette-exporter
$ pip install wheel
$ pip install hey                    ou sudo apt install hey
$ pip install werkzeug
$ pip freeze > requirements.txt
````

---
### 2. Technical choices
- *`FastAPI`*
According to the official documentation, here the advantages to use that framework : "*high performance, easy to learn, fast to code, ready for production*".
  - ***Fast*** : Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
  - ***Fast to code*** : Increase the speed to develop features by about 200% to 300%.
  - ***Fewer bugs*** : Reduce about 40% of human (developer) induced errors. *
  - ***Intuitive*** : Great editor support. Completion everywhere. Less time debugging.
  - ***Easy*** : Designed to be easy to use and learn. Less time reading docs.
  - Then, we were already familiar with flask, we wanted to try another web/api framework

- *`Hey`*
  - *Hey* is a popular tool for performing load tests on a web application.
  - *Hey* is a simple and easy to use tool for *small to medium sized load tests*, and is well suited for simple and quick tests.
  - It is enough for our use case (only one docker image to test).
  - It allows us to send HTTP requests to our web application and measure the response time of each request.
  - It is very flexible and allows us to customize many parameters, such as *the number of requests, the sending rate, the HTTP method used, the headers, the data sent in the request, etc.*

---
### 3. Create a *main.py* file
* See the *main.py* file on the repository.

---
### 4. Configuration of a *Dockerfile*

````dockerfile
FROM python:3.7-slim-buster

# RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /projet/
WORKDIR /projet/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# CMD ["bash", "-c", "uvicorn main:api_router --host 0.0.0.0 --port 80"] on Windows
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "main:api_router"]
````

---
### 5. Docker commands to build, run the project and to test the program

````bash
$ docker build --tag my-api-image:latest . # Build the image

$ docker run -p 8080:80 -it --rm my-api-image:latest # run the image
Or
$ docker run -it --network host --rm my-api-image:latest # all ports mapped by the container are locally mapped

# In another CLI terminal :
$ curl --request POST --url 'http://localhost:8080/predict' --header 'content-type: application/json' --data '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
Or
$ curl 'http://localhost:8080/predict' -H 'content-type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
````

---
### 6. Publish an image on the DockerHub *(not required)*

````bash
$ docker login --username=antoinearthur
Password : *******
Login Succeeded

$ docker images
REPOSITORY                                  TAG       IMAGE ID       CREATED        SIZE
my-api-image:latest                         latest    6194dcc249b1   40 hours ago   1.04GB

$ docker tag 6194dcc249b1 antoinearthur/app_big_data_docker_project
$ docker images
REPOSITORY                                  TAG       IMAGE ID       CREATED        SIZE
antoinearthur/app_big_data_docker_project   latest    6194dcc249b1   40 hours ago   1.04GB
my-api-image:latest                         latest    6194dcc249b1   40 hours ago   1.04GB

$ docker push antoinearthur/app_big_data_docker_project
````

* Our image, tagged with *app_big_data_docker_project*, is uploaded on the DockerHub, at the following address : https://hub.docker.com/r/antoinearthur/app_big_data_docker_project


---
### 6'.Run the image and test the program yet again

````bash
$ docker run -p 8080:80 -it --rm antoinearthur/app_big_data_docker_project

# In another CLI terminal :
$ curl 'http://localhost:8080/predict' -H 'content-type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
````

---
### 7. Configure the deployment pipeline with the following elements

#### 7.1. Build the Docker image, publish the Docker image on Azure Container Registry (ACR) and deploy it on Azure Container App

- ##### a. Configuration of a *Dockerfile* (see above)
````dockerfile
FROM python:3.7-slim-buster

# RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /projet/
WORKDIR /projet/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# CMD ["bash", "-c", "uvicorn main:api_router --host 0.0.0.0 --port 80"] on Windows
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "main:api_router"]
````

- ##### b. Configure the *GitHub Actions workflow* *(configure the autoscaling using the number of simultaneous requests as a parameter)*
  - Go to *https://github.com/efrei-ADDE92-CTP/groupe6*
  - Go to the "*Actions*" tab
  - Click on "*New workflow*" then in "*Docker image*" -> "*Configure*"
  - It allows to configure the *`docker-image.yml `* file, that can be found at :
    *https://github.com/efrei-ADDE92-CTP/groupe6/blob/main/.github/workflows/docker-image.yml*
  - Configure it as follows :
````yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - master
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: "Login via Azure CLI"
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Login to ACR
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and push image
        run: |
          docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/my-api-image:latest
          az acr build --registry ${{ secrets.REGISTRY_LOGIN_SERVER }} --image my-api-image:latest .
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/my-api-image:latest

      - name: Deploy Container App
        uses: azure/container-apps-deploy-action@47e03a783248cc0b5647f7ea03a8fb807fbc8e2f
        with:
          acrName: efreiprediction
          containerAppEnvironment: group6-env
          containerAppName: group6-container
          targetPort: 80
          resourceGroup: ${{ secrets.RESOURCE_GROUP }}
          imageToDeploy: ${{ secrets.REGISTRY_LOGIN_SERVER }}/my-api-image:latest

      - name: Configure Autoscaling
        uses: azure/CLI@v1
        with:
          inlineScript: |
            az containerapp update \
            --resource-group ${{ secrets.RESOURCE_GROUP }} \
            --name group6-container \
            --min-replicas 0 \
            --max-replicas 5 \
            --scale-rule-name azure-http-rule \
            --scale-rule-type http \
            --scale-rule-http-concurrency 100
````

- ##### c. Start the process
  - Click on "*Start commit*" then on "*Commit new file*"
  - Return to "*Actions*"
  - Click on the "*Create docker_image.yml*" workflow which is running
  - On the left side, we can see the different steps of this process, in the "*jobs*" section -> clicking on "*build*" :
    - *Set up a job*
    - *Run actions/checkout@v2*
    - *Login via Azure CLI*
    - *Login to ACR*
    - *Build and push image*
    - *Deploy Container App*
    - *Configure Autoscaling*
    - *Post Deploy Container App*
    - *Post Run actions/checkout@v2*
    - *Complete job*

=> After these steps, our image has correctly been sent to the azure portal, at the following address :
*https://portal.azure.com/#@efrei.net/resource/subscriptions/765266c6-9a23-4638-af32-dd1e32613047/resourceGroups/ADDE92-CTP/providers/Microsoft.App/containerApps/group6-container/containerapp*

---
### 8. Testing the application's scalability (observe the autoscaling)

````python
$ pip install wheel
$ pip install hey                    ou sudo apt install hey
$ pip freeze > requirements.txt
````

* We chose the *`hey`* library, easy to implement, and enough for our use case (only one docker image to test).
* See the *test_charge.py* file on the repository.

````bash
# On the first CLI terminal :
$ docker run -p 8080:80 -it --rm my-api-image:latest
Or
$ docker run -p 8080:80 -it --rm antoinearthur/app_big_data_docker_project
````

````python
# On another CLI terminal :
$ python test_charge.py
````

* On the first CLI terminal :
````bash
INFO:     172.17.0.1:36380 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     172.17.0.1:36234 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     172.17.0.1:36384 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     172.17.0.1:35866 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
````

* On the second CLI terminal :
````bash
Summary:
  Total:        7.2684 secs
  Slowest:      
  Fastest:      0.0014 secs
  Average:      0.0718 secs
  Requests/sec: 1375.8257

  Total data:   810000 bytes
  Size/request: 81 bytes

Response time histogram:
  0.001 [1]     |
  0.018 [32]    |
  0.034 [214]   |■■
  0.051 [376]   |■■■■
  0.067 [4101]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.084 [3552]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.101 [743]   |■■■■■■■
  0.117 [659]   |■■■■■■
  0.134 [123]   |■
  0.150 [99]    |■
  0.167 [100]   |■


Latency distribution:
  10% in 0.0587 secs
  25% in 0.0611 secs
  50% in 0.0682 secs
  75% in 0.0775 secs
  90% in 0.0990 secs
  95% in 0.1085 secs
  99% in 0.1542 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0005 secs, 0.0014 secs, 0.1666 secs
  DNS-lookup:   0.0002 secs, 0.0000 secs, 0.0530 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0045 secs
  resp wait:    0.0711 secs, 0.0013 secs, 0.1387 secs
  resp read:    0.0001 secs, 0.0000 secs, 0.0057 secs

Status code distribution:
  [422] 10000 responses
````

* *Interpretation of the results* :
  - Total process time: 7.2684 secs.
  - Fastest response: 0.0014 secs.
  - Slowest response: 0.1666 secs.
  - Average response time of our requests: 0.0718 secs.
  - 50% of our requests have a maximum response time of 0.0682 secs.
  - Requests/sec: 1375.8257

---
### 9. Get the Endpoint API of your Azure Container App *(ACA)*

On *Azure Portal*, go to :
- "*All resources*"
- "*Subscription*" -> *"Efrei - Apprentis BDML*" -> "*groupe6-container*"
- "*Overview*" or "*Input*"
- "*Properties*" -> "*Networking*" -> click on "*deactivated*"
- "*Input*" -> check "*activated*"
- "*Unsecured connections*" -> "*Authorized*"
- "*Destination port*" -> "*80*"
- "*Save*" and return to "*Overview*"
- Copy the application url (endpoint api of the *ACA*) : https://group6-container.ashycliff-15f451bd.westeurope.azurecontainerapps.io
- Go to "*Logs*" -> type "*ContainerAppConsoleLogs_CL*" into the console
- We have access to logs which show us that the deployment went well and that the server is running (cf *img/endpoint_api_aca.png*)

*We obtain the same results as for the previous runs.*
For instance, we can test our `/metrics` endpoint and see that it returns the same information as before, by going to the following URL :
https://group6-container.ashycliff-15f451bd.westeurope.azurecontainerapps.io/metrics (cf *img/ACAendpointcall2.JPG*).

Finally, by performing a "*curl*" command in a local terminal, we get the same result as before :
````bash
curl 'https://group6-container.ashycliff-15f451bd.westeurope.azurecontainerapps.io/predict' -H 'content-type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}
````
 (cf *img/ACAendpointcall.png*)

---
### 10.1. Use a linter for Dockerfile in the deployment pipeline to ensure its consistency

- We use the Dockerfile linter named *`hadolint`*.
- In the *`docker_image.yml`* file, we add these lines :
````yaml
- name: Linter Dockerfile
  uses: hadolint/hadolint-action@v2.0.0
  with:
    dockerfile: Dockerfile
````

- This "*Dockerfile linter*" step pulls a "*hadolint Docker image*" and uses it to linter the Dockerfile. If the linter detects any problems, the build will fail.
  - It allows us to check that our Dockerfile is correctly written (respect of good practices).
  - It means that once we have configured our deployment pipeline to use a Dockerfile linter, we can be sure that all the Docker images we deploy are up to quality standards.

- We can see this with the add of these lines in the jobs process steps :
    - *Set up a job*
    - ***Build hadolint/hadolint-action@v2.0.0***
    - *Run actions/checkout@v2*
    - ***Linter Dockerfile***
    - *Login via Azure CLI*
    - *Login to ACR*
    - *Build and push image*
    - *Deploy Container App*
    - *Configure Autoscaling*
    - *Post Deploy Container App*
    - *Post Run actions/checkout@v2*
    - *Complete job*

---
### 10.2. Set up a local prometheus stack to scrape and store your exposed metrics

On a second CLI terminal, we have to type :

````bash
WSL2 :
arthur@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet$

$ cd prometheus
arthur@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet/prometheus$

$ sudo chmod a+rx prometheus.exe # on Windows
Or
$ sudo chmod a+rx prometheus # on Linux
[sudo] password for arthur:

arthur@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet/prometheus$
$ ./prometheus.exe # on Windows
Or
$ prometheus --config.file=prometheus.yml --storage.tsdb.path=/tmp/prometheus # on Windows or Linux
````

- Go to ***http://localhost:9090*** (or ***http://localhost:9090/graph***)
- Then, go to ***http://localhost:9090/targets***
- Finally, click on : ***http://localhost:8080/metrics***
  We have access to our `/metrics` endpoint, as before (cf *prometheus3.JPG*).

Here is a summary of the different steps :

````bash
# On the first CLI terminal :
$ docker run -p 8080:80 -it --rm my-api-image:latest
Or
$ docker run -p 8080:80 -it --rm antoinearthur/app_big_data_docker_project

# On the second CLI terminal :
$ ./prometheus.exe
Or
$ prometheus --config.file=prometheus.yml --storage.tsdb.path=/tmp/prometheus

# On the third CLI terminal :
curl http://localhost:8080/metrics
````

With that last command on the third CLI, We have access to our `/metrics` endpoint on the CLI, as before.
