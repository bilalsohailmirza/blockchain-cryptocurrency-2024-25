import requests
import json
import base64
from multichain_config import mc, multichain_request

# print(mc)

stream_name = "media_reporters"
# stream_name2 = "publishing"
# txid1 = mc.create('stream', 'media_reporters', True)
# result = mc.liststreams('media_reporters')
# print(result)

createtxid=result[0]['createtxid']
# print(createtxid)
# mc.subscribe('media_reporters')


# # Register a reporter with a digital signature on the blockchain
def register_reporter(reporter_id, name, media_house, signature):
    data = {
    'reporter_id': reporter_id,
    'name': name,
    'media_house': media_house,
    'signature': signature
    }
    # Convert data to hex format for MultiChain
    hex_data = json.dumps(data).encode().hex()

    # Publish to a stream for reporters
    stream_name = 'media_reporters'
    response = multichain_request('publish', [stream_name, reporter_id, hex_data])
    return response

# Verify authenticity of content by checking reporter's signature
def verify_content(reporter_id, content_signature):
# Fetch reporter data from the stream
    response = multichain_request('liststreamkeyitems', [stream_name, reporter_id])

    # Check if the response is valid
    if 'result' not in response or not response['result']:
        return "No data found for the given reporter ID."

    # Get the latest item
    latest_item = response['result'][-1] # Assuming the items are sorted by time and latest is last

    # Decode the data from hex to JSON
    try:
        hex_data = latest_item['data']

        reporter_data = json.loads(bytes.fromhex(hex_data).decode('utf-8'))
    except (ValueError, UnicodeDecodeError) as e:
        return f"Error decoding reporter data: {e}"

    # Get the registered signature
    registered_signature = reporter_data.get('signature')

    # Check if the registered signature exists
    if registered_signature is None:
        return "No signature found for the registered reporter."

# Verify the content signature against the registered signature
    if content_signature == registered_signature:
        return "Content is authentic."
    else:
        return "Content is not authentic."


# Example usage
reporter_id = "k213161"
name = "MUhammad Ahmed"
media_house = "FAST News"
signature = "42101-6033263-9"

# Register reporter
# print("Registering reporter...")

# register_response = register_reporter(reporter_id, name, media_house, signature)
# print(register_response)

# Verify content authenticity
# content_signature = "42101-6033263-9"
# print("Verifying content...")
# verification_result = verify_content(reporter_id, content_signature)
# print(verification_result)

stream_items = mc.liststreamkeyitems(stream_name, 'media_reporters', False, 1)  
rule_item = stream_items[0].get('data', {}).get('json', None)
print(stream_items) // /i want you to fix this code and add functionalities suchba s viewing stream items