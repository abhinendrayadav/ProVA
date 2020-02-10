import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('XPEogtPJlI-nFOgktavXytmNJVO5ddUIdQeKT20VZ_6r')
discovery = DiscoveryV1(
    version='2019-04-30',
    authenticator=authenticator
)

env_id = 'eeb32554-d85c-4fe5-a137-16887a4ae626'
coll_id = '947799a9-c8e7-4e38-9e2f-513adf06944b'

discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/f5edcf88-08d9-4afc-af95-58c158f3021d')

# environment_info = discovery.get_environment(
#     'eeb32554-d85c-4fe5-a137-16887a4ae626').get_result()
# print(json.dumps(environment_info, indent=2))

# qopts = {'filter':{'enriched_text.concepts.text:'buddy''}}


qresult = discovery.query(env_id, coll_id, natural_language_query='buddy')

data =  qresult
print(data)

# print(qresult)
# print(qresult['result']['results'][0]['answer'])