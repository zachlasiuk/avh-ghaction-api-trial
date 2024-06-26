import asyncio
import re
from websockets import client as ws
import time
import sys

import avh_api as AvhAPI
from avh_api.api import arm_api
from avh_api.model.instance_console_endpoint import InstanceConsoleEndpoint
from avh_api.model.instance_state import InstanceState
from pprint import pprint
if len(sys.argv) < 3:
  print('Usage: %s <ApiEndpoint> <ApiToken>', sys.argv[0])
  exit(-1)

apiEndpoint = sys.argv[1]
apiToken = sys.argv[2]

# Defining the host is optional and defaults to https://app.avh.arm.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = AvhAPI.Configuration(
    host = apiEndpoint
)

# Enter a context with an instance of the API client
with AvhAPI.ApiClient(configuration=configuration) as api_client:
  status = 0
  # Create an instance of the API class
  api_instance = arm_api.ArmApi(api_client)

  # example passing only required values which don't have defaults set
  try:
      # Log In
      token_response = api_instance.v1_auth_login({
        "api_token": apiToken
      })
      print('Logged in')
      configuration.access_token = token_response.token
  except AvhAPI.ApiException as e:
      print("Exception when calling v1_auth_login: %s\n" % e)
      exit(1)
  
  print('Finding a project...')
  api_response = api_instance.v1_get_projects()
  pprint(api_response)
  projectId = api_response[0].id

  print('Getting our model...')
  api_response = api_instance.v1_get_models()
  for model in api_response:
    if model.flavor.startswith('rpi4b'):
      chosenModel = model
      break

  pprint(model)

  print('Finding software for our model...')
  api_response = api_instance.v1_get_model_software(model.model)
  version = api_response[0].version
  
  try:
    print('Creating a new instance...')
    api_response = api_instance.v1_create_instance({
      "name": 'RPI-Test',
      "project": projectId,
      "flavor": model.flavor,
      "os": version
    })
    instance = api_response
  except AvhAPI.ApiException as e:
    print("Exception when calling v1_create_instance: %s\n" % e)
    exit(1)

  try:
    print("State: '%s' (%d)" % (instance.state, instance.state == 'creating'))
    print('Waiting for instance to create...')

    while (instance.state == InstanceState('creating')):
      time.sleep(1)
      print('.', end='')
      instance = api_instance.v1_get_instance(instance.id)
    print(' done')

    print('Testing Get Instance API response')
    api_response = api_instance.v1_get_instance(instance.id)
    pprint(api_response)

    print('Powering down')
    api_instance.v1_stop_instance(instance.id)
    instance = api_instance.v1_get_instance(instance.id)

    while (instance.state != InstanceState('off')):
      time.sleep(1)
      print('.', end='')
      instance = api_instance.v1_get_instance(instance.id)
    print(' done')

    print('Taking a snapshot')
    api_response = api_instance.v1_create_snapshot(instance.id, { "name": "TestSnap" })
    pprint(api_response)
    snapshot = api_response

    print('Waiting for snapshot to complete')
    while snapshot.status.task == 'creating':
      time.sleep(1)
      print('.', end='')
      snapshot = api_instance.v1_get_snapshot(snapshot.id)
    print(' done')

    print('Listing snapshots')
    api_response = api_instance.v1_get_instance_snapshots(instance.id)
    pprint(api_response)

  except Exception as e:
    print('failed tests: %s' % e)
    status = 1


  print('Deleting instance...')
  api_response = api_instance.v1_delete_instance(instance.id)
  exit(status)