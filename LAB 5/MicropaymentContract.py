import json
import base64
import multichain

# Step 1: Load the JSON data (rule) from file or create it programmatically
rule = {
    "balance": 100,
    "server_approval": False,
    "txid": "",
}

# Step 2: Convert JSON data to string and then encode it to base64
rule_json_str = json.dumps(rule)
rule_base64 = base64.b64encode(rule_json_str.encode('utf-8')).decode('utf-8')

# Step 3: Define Multichain node details
rpcuser = "multichainrpc"  # Replace with your Multichain RPC user
rpcpassword = "9h4UVx1pihBeTa7CmptRx2pV1k5Zcdh9NJcCY86zGza2"  # Replace with your RPC password
rpchost = "127.0.0.1"  # Localhost where Multichain node is running
rpcport = 6792  # Multichain node RPC port
chainname = "ahmed"  # Name of the Multichain chain

mc = multichain.MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

def return_mc():
    return mc

def return_rule_item():
    stream_name = "micropayment_stream"
    stream_items = mc.liststreamkeyitems(stream_name, 'key1', False, 1)  
    
    if stream_items:
        rule_item = stream_items[0].get('data', {}).get('json', None)
        if rule_item:
            return rule_item
        else:
            return "No valid JSON data found in the stream item."
    else:
        return "No items found in the stream."

if __name__ == '__main__':
    stream_name = "micropayment_stream"  
    # txid1 = mc.create('stream', 'micropayment_stream', True) 
    mc.subscribe(stream_name)
    mc.publish('micropayment_stream', 'key1', {'json': rule })

    stream_items = mc.liststreamkeyitems(stream_name, 'key1', False, 1) 
    print(stream_items)
    updated_rule_item = return_rule_item()
  
    if stream_items:
        updated_rule_item = stream_items[0].get('data', {}).get('json', None)

        if updated_rule_item:
            with open('micropayment.json', 'w') as json_file:
                json.dump(updated_rule_item, json_file, indent=4)
                print("Rule saved to 'micropayment.json'.")
            print(f"Fetched rule: {updated_rule_item}")
        else:
            print("No valid JSON data found in the stream item.")
    else:
        print("No items found in the stream.")

 