# balenaRancher/rancher/token-wrangler.py
# Sam Dennon//2022

import os
from time import sleep
from os.path import exists, isfile
import balena

token_path = '/var/lib/rancher/k3s/server/node-token'
var = 'K3S_TOKEN'
app_id = os.environ.get('BALENA_APP_ID')
token = os.environ.get('BALENA_API_KEY')
api = balena.Balena()
appVariables = api.models.environment_variables.application

def getAppVars(app_id, token):
  try: api.auth.login_with_token(token)
  except ValueError: print('Mistakes were made, check your API key.')
  try: return appVariables.get_all(app_id)
  except ValueError: print('Mistakes were made, unable to get fleet variable list')
    
def getVarId(app_id, token, var):
  try: return [i['id'] for i in getAppVars(app_id, token) if i['name'] == var]
  except ValueError: print('Mistakes were made, unable to do the thing...')

def updateOrAddAppVar(app_id, token, var, var_val):
  try: 
    if var in [i['name'] for i in getAppVars(app_id, token)]:
      appVariables.update(getVarId(app_id, token, var)[0], var_val)
    else:
      appVariables.create(app_id, var, var_val)
  except ValueError: print('Nope, did not work.')

while not exists(token_path):
  sleep(2)

if isfile(token_path, var):
  var_val = open(token_path, 'r').read().strip()
  updateOrAddAppVar(app_id, token, var, var_val)
else:
  print('I done effed up, Sarge.')
