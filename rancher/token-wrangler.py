import os
from time import sleep
from os.path import exists, isfile 
import balena

TOKEN_PATH = '/var/lib/rancher/k3s/server/node-token'
BALENA_APP_ID = os.environ.get('BALENA_APP_ID')
BALENA_API_KEY = os.environ.get('BALENA_API_KEY')
api = balena.Balena()

def createSuperToken(token):
  api.auth.login_with_token(BALENA_API_KEY)
  fleet_vars = api.models.environment_variables.application.get_all(BALENA_APP_ID)
  list_from = [i['name'] for i in fleet_vars]
  var_id = [i['id'] for i in fleet_vars if i['name'] == 'K3S_TOKEN']
  if 'K3S_TOKEN' in list_from:
    api.models.environment_variables.application.update(var_id[0], token)
  else:
    api.models.environment_variables.application.create(BALENA_APP_ID, 'K3S_TOKEN', token)


while not exists(TOKEN_PATH):
  sleep(2)

if isfile(TOKEN_PATH):
  token = open(TOKEN_PATH, 'r')
  createSuperToken(token.read())
else:
  print('I done effed up, Sarge.')