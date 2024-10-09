import requests
import json
import base64
from multichain_config import mc, multichain_request

stream_name = "media_reporters"
stream_name2 = "report"

# Fetch and print stream creation txid for stream_name2
result = mc.liststreams(stream_name2)
reporter = result[0]['createtxid']
print(f"Reporter Signature: {reporter}")

    # data = {
    #     'reporter_id': reporter_id,
    #     'conf_true': 0.5,
    #     'conf_false': 0.5,
    #     'text': "The stock market has seen an unprecedented rise today due to new policies."
    # }


# Register a reporter with a digital signature on the blockchain
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
    response = multichain_request('publish', [stream_name, reporter_id, hex_data])
    return response

# Verify authenticity of content by checking reporter's data
def verify_content(reporter_id, conf_ratio):
    # Fetch reporter data from the report stream
    response = multichain_request('liststreamkeyitems', [stream_name2, reporter_id])
    # print(response)
    # Check if the response is valid
    if 'result' not in response or not response['result']:
        return "No data found for the given reporter ID."

    # Get the latest item
    latest_item = response['result'][-1]  # Assuming the latest item is the last one in the result

    # Decode the data from hex to JSON
    try:
        hex_data = latest_item['data']
        reporter_data = json.loads(bytes.fromhex(hex_data).decode('utf-8'))
    except (ValueError, UnicodeDecodeError) as e:
        return f"Error decoding reporter data: {e}"

    # Print the fetched reporter data
    print(f"Reporter Data: {reporter_data}")
    
    # Example confidence check (using `conf_ratio` for additional logic if needed)
    if reporter_data.get('conf_true') >= conf_ratio:
        return "Content is likely authentic based on confidence ratio."
    else:
        return "Content is unlikely to be authentic."

# View stream items for a specific key
def view_stream_items(reporter_id, count=10):
    # Fetch the stream items for the given reporter_id from stream_name2
    response = multichain_request('liststreamkeyitems', [stream_name, reporter_id, False, count])
    
    # Check if the response is valid
    if 'result' not in response or not response['result']:
        return f"No items found for the reporter ID: {reporter_id}"

    # Loop through the items and print them
    items = []
    for item in response['result']:
        try:
            # Decode the hex data
            hex_data = item['data']
            reporter_data = json.loads(bytes.fromhex(hex_data).decode('utf-8'))
            items.append(reporter_data)
        except (ValueError, UnicodeDecodeError) as e:
            items.append(f"Error decoding item data: {e}")

    return items

# Add a dummy stream item to stream_name2
def add_dummy_report_item(reporter_id):
    # Create dummy data
    data = {
    'reporter_id': reporter_id,
    'conf_true': 0.5,
    'conf_false': 0.5,
    'text': "The stock market has seen an unprecedented rise today due to new policies."
    }
    # Convert data to hex format for MultiChain
    hex_data = json.dumps(data).encode().hex()

    # Publish the dummy data to the report stream (stream_name2)
    response = multichain_request('publish', [stream_name2, reporter_id, hex_data])
    return response

# Example usage
reporter_id = "k213161"
# add_response = add_dummy_report_item(reporter_id)
# print(f"Added dummy report item: {add_response}")


# Example usage
# reporter_id = "k213161"

stream_items = view_stream_items(reporter_id, 5)  # Fetch the latest 5 items
print(f"Stream Items: {stream_items}")

verification_result = verify_content(reporter_id, 0.9)
print(f"Verification Result: {verification_result}")
