import multichain

rpcuser = "multichainrpc"
rpcpassword = "9h4UVx1pihBeTa7CmptRx2pV1k5Zcdh9NJcCY86zGza2"
rpchost = "127.0.0.1"
rpcport = 6792
chainname = "ahmed"

mc=multichain.MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# MultiChain helper function for making requests

def multichain_request(method, params=None):
    if params is None:
        params = []
    headers = {'content-type': 'application/json'}
    payload = json.dumps({
        "method": method,
        "params": params,
        "id": 1,
        "jsonrpc": "2.0"
    })
    response = requests.post(node_url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
    
    return response.json()
