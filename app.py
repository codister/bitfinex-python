#PYTHON 3.4
import requests
import json
import base64
import hashlib
import time
import hmac

DEPOSIT_API_URL = 'https://api.bitfinex.com/v1/deposit/new' # This has to be change wrt API endpoint! 
bitfinexKey = ''
bitfinexSecret = b'' #the b is deliberate, encodes to bytes

def main():
    print("BitFinex Generate a New Address for Deposit")
    payloadObject = {
            'request':'/v1/deposit/new',
            'nonce':str(time.time() * 1000000), #convert to string
            'method':'bitcoin',
            'wallet_name':'deposit',
            'renew':0
    }

    payload_json = json.dumps(payloadObject)
    print("payload_json: ", payload_json)

    payload = base64.b64encode(bytes(payload_json, "utf-8"))
    print("payload: ", payload)

    m = hmac.new(bitfinexSecret, payload, hashlib.sha384)
    m = m.hexdigest()

    #headers
    headers = {
          'X-BFX-APIKEY' : bitfinexKey,
          'X-BFX-PAYLOAD' : payload,
          'X-BFX-SIGNATURE' : m
    }

    r = requests.get(DEPOSIT_API_URL, data={}, headers=headers)
    print('Response Code: ' + str(r.status_code))
    #print('Response Header: ' + str(r.headers))
    print('Response Content: '+ str(r.content))

    ## Check the Balance History
    ############################

    API_HISTORY_URL = 'https://api.bitfinex.com/v1/history'
    print("Check if the Payment is Completed")
    payloadObject = {
            'request':'/v1/history',
            'nonce':str(time.time() * 1000000), #convert to string
            'currency':'btc',
    }

    payload_json = json.dumps(payloadObject)
    print("payload_json: ", payload_json)

    payload = base64.b64encode(bytes(payload_json, "utf-8"))
    print("payload: ", payload)

    m = hmac.new(bitfinexSecret, payload, hashlib.sha384)
    m = m.hexdigest()

    #headers
    headers = {
          'X-BFX-APIKEY' : bitfinexKey,
          'X-BFX-PAYLOAD' : payload,
          'X-BFX-SIGNATURE' : m
    }

    r = requests.get(API_HISTORY_URL, data={}, headers=headers)
    print('Response Code: ' + str(r.status_code))
    #print('Response Header: ' + str(r.headers))
    print('Response Content: '+ str(r.content))

main()