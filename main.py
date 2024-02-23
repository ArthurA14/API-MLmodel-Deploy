from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
import uvicorn
from starlette.responses import JSONResponse, Response
from starlette.middleware import Middleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client import Counter, Histogram, Info, Summary, generate_latest, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import prometheus_client
import joblib
import schemas
import pandas as pd
import numpy as np
import json
import time


api_router = FastAPI() # APIRouter()
api_router.add_middleware(PrometheusMiddleware)
api_router.add_route("/metrics", handle_metrics)

# Add Prometheus middleware to the FastAPI application
middleware = [Middleware(PrometheusMiddleware)]
api_router = FastAPI(middleware=middleware)

with open('rf.sav', 'rb') as file :
    loaded_model = joblib.load(file)

# Define the metric variables
predict_calls_counter = Counter('total_predict_calls', 'Number of predict requests to the API endpoint', ['method', 'endpoint'])
predict_call_duration = Histogram('predict_latency_seconds', 'Latency time of the API for a predict call', ['method']) # ValueError: No label names were set when constructing histogram:predict_latency_seconds
api_call_info = Info('api_info', 'Information about the API', ["method", "second_endpoint"])
api_call_summary = Summary('api_call_bytes_size', 'Size of the API call', ["method", "third_endpoint"])


############################################################ PREDICT #################################################################

@api_router.post("/predict", status_code=200)
async def predict(input_data: schemas.Iris) :
    """
    Make predictions with the Fraud detection model
    """

    start_time = time.time()
    
    # Convert input type schemas.Iris to JSON object and then into a Python object, with json.loads()
    data = json.loads(input_data.json()) # JSON -> Python

    # Extract only values and convert them to numpy 
    X = np.array(list(data.values())).reshape(1, -1)

    # Get prediction
    pred = loaded_model.predict(X) # -> numpy.ndarray type

    # Labels
    iris_labels = ['iris setosa', 'iris versicolor', 'iris virginica']

    # Convert Python object into a string in JSON object format
    # json_pred = json.dumps(pred.tolist()) # Python -> JSON str type
    # iris_pred = iris_labels[int(float(json_pred[1:-1]))] # '[2.0]' ValueError: invalid literal for int() with base 10: '2.0'

    # Get the prediction label
    iris_pred = iris_labels[int(pred[0])] # TypeError: list indices must be integers or slices, not numpy.float64
    labeled_pred = {'prediction': iris_pred, 'score': pred[0]}

    # Increment the counter
    predict_calls_counter.labels('POST', '/predict').inc()

    # Get the request time duration
    predict_call_duration.labels(pred).observe(time.time() - start_time)

    print("Prediction is : ", labeled_pred)
    return json.dumps(labeled_pred) # return labeled_pred # pred.tolist()
    # curl 'http://localhost:8080/predict' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'


############################################################ METRICS #################################################################

# Define the metrics endpoint
@api_router.get("/metrics")
async def metrics() :
    return Response(content=generate_latest(), media_type='text/plain') # return generate_latest().decode("utf-8")
    # curl 'http://localhost:8080/metrics' -H 'Content-Type: application/json'| tr -d '\n' | tr '#' '\n' | grep -v '^$'


@api_router.post("/metrics/calls_count")
async def get_counter() :
    return generate_latest(predict_calls_counter).decode("utf-8")
    # curl 'http://localhost:8080/metrics/calls_count' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}' | tr -d '\n' | tr '#' '\n' | grep -v '^$'


@api_router.post('/metrics/duration')
async def get_duration() :
    return generate_latest(predict_call_duration).decode("utf-8")
    # curl 'http://localhost:8080/metrics/duration' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}' | tr -d '\n' | tr '#' '\n' | grep -v '^$'


@api_router.post("/api/call/info")
async def api_call_info_post() :
    endpoint = "/api/call/info"
    api_call_info.labels("POST", "info").info({"endpoint": endpoint, "info": api_call_info.info})
    return {"status": "success"}
    # curl 'http://localhost:8080/api/call/info' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}' | tr -d '\n' | tr '#' '\n' | grep -v '^$'


@api_router.post("/api/call/summary")
async def api_call_summary_post() :
    start = time.time()
    # Perform API processing here
    api_call_summary.labels("POST", "elapsed_time").observe(time.time() - start)
    return {"status": "success"}
    # curl 'http://localhost:8080/api/call/summary' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}' | tr -d '\n' | tr '#' '\n' | grep -v '^$'



if __name__ == '__main__' :
    uvicorn.run(api_router, host="0.0.0.0", port=8080) # api_router.run(debug=False, host='0.0.0.0', port=8080) with Flask