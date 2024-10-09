import json
import base64
import multichain

# Step 1: Load the JSON data (rule) from file or create it programmatically
rule = {
    "balance": 100,
    "bob_approval": False,
    "alice_approval": False
}

# Step 2: Convert JSON data to string and then encode it to base64
rule_json_str = json.dumps(rule)
rule_base64 = base64.b64encode(rule_json_str.encode('utf-8')).decode('utf-8')

# Step 3: Define Multichain node details
rpcuser = "multichainrpc"  # Replace with your Multichain RPC user
rpcpassword = "A1yGRjm65hFj24CsTc7BDLC1JvviMme62d88kXxQqhri"  # Replace with your RPC password
rpchost = "127.0.0.1"  # Localhost where Multichain node is running
rpcport = 7750  # Multichain node RPC port
chainname = "bilal"  # Name of the Multichain chain

# Step 4: Initialize the MultiChainClient
mc=multichain.MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)
# Step 5: Define stream name
stream_name = "escrow_rules_stream"  # Name of the stream

txid1 = mc.create('stream', 'escrow_rules_stream', True) # open to all to writetxid12=	mc.create('stream', 'LocalServiceAgreement', True)
        
	#result = mc.getstreaminfo('Localrule')
	#result = mc.liststreams() # all streams


result = mc.liststreams('escrow_rules_stream') # one specific stream
print(result)
mc.subscribe('escrow_rules_stream')

txid2 = mc.publish(stream_name, 'key1', {'json': rule}) 
print(txid2)
