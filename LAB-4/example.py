import json
import os
import multichain

######################################Server Connection############################
rpcuser = "multichainrpc"
rpcpassword = "EDGoksjPRZA12aFaYmmJ21SXyTWMuhA3Nz7p6Y2rJxrE"
rpchost = "127.0.0.1"
rpcport = "6830"
chainname = "test"
mc=multichain.MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)
result = mc.getaddresses()
print(result)