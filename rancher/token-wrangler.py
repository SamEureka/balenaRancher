## balenaRancher/rancher/token-wrangler.py
## Sam Dennon//2022
## Updated 01MAY2023 // Cleaned up api use to reduce calls

import os
import re
from time import sleep
from os.path import exists, isfile
import balena

# Change these variables to the Application Environment Variable that you want to add/update
token_path = '/var/lib/rancher/k3s/server/node-token'
token_var_name = 'K3S_TOKEN'
url_var_name = 'K3S_URL'

# Make sure you get an API key at: [access-tokens](https://dashboard.balena-cloud.com/preferences/access-tokens) 
# Then create a Fleet Variable called API_KEY. Do this before adding your Rancher server.
app_id = os.environ.get('BALENA_APP_ID')
uuid = os.environ.get('BALENA_DEVICE_UUID')
token = os.environ.get('API_KEY')
api = balena.Balena()
appVariables = api.models.environment_variables.application
device = api.models.device

# Login API and store the token
api.auth.login_with_token(token)
auth_token = api.auth.token

def generateURL(uuid):
  for ip_add in device.get_local_ip_address(uuid):
    if not re.search('10.42', ip_add):
      return 'https://{}:6443'.format(ip_add)

def getAppVars(app_id):
  return appVariables.get_all(app_id)
      
def getVarId(app_id, var):
  return [i['id'] for i in getAppVars(app_id) if i['name'] == var]
  
def updateOrAddAppVar(app_id, var, var_val):
  if var in [i['name'] for i in getAppVars(app_id)]:
    appVariables.update(getVarId(app_id, var)[0], var_val)
  else:
    appVariables.create(app_id, var, var_val)

while not exists(token_path):
  sleep(2)

if isfile(token_path):
  var_val = open(token_path, 'r').read().strip()
  updateOrAddAppVar(app_id, token_var_name, var_val)
  updateOrAddAppVar(app_id, url_var_name, generateURL(uuid))
else:
  print('I done effed up, Sarge. There aint no file here...')

# Logout API
api.auth.logout(auth_token)
