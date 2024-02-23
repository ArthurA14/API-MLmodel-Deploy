# import json
import subprocess

url = 'http://localhost:8080/predict'
# headers = {"content-type": "application/json"}
# data = {"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}
# # convertir le dictionnaire en une chaîne de caractères de format JSON avant de l'inclure dans la commande.
# data_json = json.dumps(data)

# cmd = f'hey -n 10000 -c 100 -m POST -H \'content-type: application/json\' -d \'{{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}}\' http://localhost:8080/predict'
# cmd = f'hey -n 10000 -c 100 -m POST -H \'content-type: {headers["content-type"]}\' -d \'{data_json}\' {url}'
cmd = f'hey -n 10000 -c 100 -m POST {url}'
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if error:
    print(f'An error occurred: {error}')
else:
    print(output.decode('utf-8'))

####################################################################

# cmd = 'hey -n 10000 -c 100 http://0.0.0.0:8080'
# process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()

# if error:
#     print(f'An error occurred: {error}')
# else:
#     print(output.decode('utf-8'))

####################################################################

# import requests

# url = 'http://0.0.0.0:8080'

# for i in range(10):
#     response = requests.get(url)
#     print('Response code:', response.status_code)