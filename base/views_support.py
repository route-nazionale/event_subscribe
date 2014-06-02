
from django.http import HttpResponse

import json

HttpJSONResponse = lambda x : HttpResponse(
    json.dumps(x), mimetype="application/json"
)

# create a JSON response to POST
def API_response(status="OK", message=''):
    data = {
        'status' : status,
        'message' : message
    }
    return HttpJSONResponse(data)

def API_ERROR_response(message):
    return API_response("ERROR", message)
