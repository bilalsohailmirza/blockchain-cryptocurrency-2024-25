#   MultiChain JSON-RPC API Library for Python
#   
#   Copyright (c) Coin Sciences Ltd - www.multichain.com
#   
#   All rights reserved under BSD 3-clause license
#   
#   Examples of Python library usage, for more details see:
#   https://www.multichain.com/developers/json-rpc-api/


exit() # in case this file is included accidentally!


#########################
##  General utilities  ##
#########################

result = mc.getblockchainparams()
result = mc.gethealthcheck()
result = mc.getruntimeparams()
mc.setruntimeparam('maxshowndata', 16384) # no result, check mc.success()
result = mc.getinfo()
result = mc.getinitstatus()


#################################
##  Managing wallet addresses  ##
#################################

address = mc.addmultisigaddress(2, [address1, address2])
result = mc.getaddresses()
address = mc.getnewaddress()

mc.importaddress(address) # no result, check mc.success()
mc.importaddress([address1, address2]) # no result, check mc.success()

result = mc.listaddresses() # all addresses
result = mc.listaddresses(address) # one specific address
result = mc.listaddresses([address1, address2]) # multiple specific addresses


#########################################
##  Working with non-wallet addresses  ##
#########################################

result = mc.createkeypairs()
result = mc.createmultisig(2, [address1, address2])

result = mc.validateaddress(address)
result = mc.validateaddress(privkey)


##############################
##  Permissions management  ##
##############################

txid = mc.grant(address, 'send,receive') # global permission
txid = mc.grant(address, 'stream1.write') # per-entity permission
txid = mc.grant(address1+','+address2, 'connect') # multiple addresses
txid = mc.grantfrom(fromaddress, address, 'create')

# see online API documentation for many more ways to attach data
txid = mc.grantwithdata(address, 'connect', 'a1b2c3d4') # raw binary data
txid = mc.grantwithdata(address, 'connect', {'for' : 'stream1', 'keys' : ['key1'], 'data' : {'json' : {'name' : 'Mary'}}}) # JSON stream item
txid = mc.grantwithdatafrom(frommaddress, address, 'issue', 'a1b2c3d4')

result = mc.listpermissions() # all permissions
result = mc.listpermissions('send,receive') # specific permissions
result = mc.listpermissions('*', address) # one specific address
result = mc.listpermissions('*', [address1, address2]) # multiple specific addresses

txid = mc.revoke(address, 'send,receive')
txid = mc.revokefrom(fromaddress, address, 'create')

result = mc.verifypermission(address, 'send')


########################
##  Asset management  ##
########################

result = mc.getassetinfo('asset1')
result = mc.gettokeninfo('asset1', 'token1')

# see online API documentation for many more options when issuing an asset
txid = mc.issue(address, {'name' : 'asset1'}, 1000, 0.01) # fungible asset
txid = mc.issue(address, {'name' : 'asset1', 'open' : True}, 1000, 0.01) # allow reissuance
txid = mc.issue(address, {'name' : 'asset1'}, 1000, 0.01, 0, {'origin' : 'US'}) # custom fields
txid = mc.issue(address, {'name' : 'nfts1', 'fungible' : False, 'open' : True}, 0, 1) # non-fungible asset
txid = mc.issuefrom(fromaddress, address, {'name' : 'asset1'}, 1000, 0.01) # fungible asset

txid = mc.issuemore(address, 'asset1', 100)
txid = mc.issuemore(address, 'asset1', 100, 0, {'origin' : 'EU'}) # custom fields
txid = mc.issuemorefrom(fromaddress, address, 'asset1', 100)

txid = mc.issuetoken(address, 'nfts1', 'token1', 1)
txid = mc.issuetoken(address, 'nfts1', 'token1', 1, 0, {'origin' : 'UK'}) # token details
txid = mc.issuetokenfrom(fromaddress, address, 'nfts1', 'token1', 1)

result = mc.listassetissues('asset1')
result = mc.listassetissues('asset1', False, 10, 30) # paging through issues

result = mc.listassets() # all assets
result = mc.listassets('asset1') # one specific asset
result = mc.listassets(['asset1', 'asset2']) # multiple specific assets
result = mc.listassets('*', False, 10, 30) # paging through assets

txid = mc.update('asset1', {'open' : True})
txid = mc.updatefrom(fromaddress, 'asset1', {'open' : False})


#################################################
##  Querying wallet balances and transactions  ##
#################################################

result = mc.getaddressbalances(address)
result = mc.getaddressbalances(address, 0) # including unconfirmed transactions

result = mc.getmultibalances() # all addresses, all assets
result = mc.getmultibalances(address) # one specific address
result = mc.getmultibalances([address1, address2]) # multiple specific addresses
result = mc.getmultibalances('*', 'asset1') # one specific asset
result = mc.getmultibalances('*', ['asset1', 'asset2']) # multiple specific assets
result = mc.getmultibalances('*', '*', 0) # including unconfirmed transactions
result = mc.getmultibalances('*', '*', 1, True) # including watch-only addresses

# the gettokenbalances command supports all the same parameters as getmultibalances
result = mc.gettokenbalances() # all addresses, all non-fungible assets

result = mc.gettotalbalances()
result = mc.gettotalbalances(0) # including unconfirmed transactions
result = mc.gettotalbalances(1, True) # including watch-only addresses

result = mc.getaddresstransaction(address, txid)
result = mc.getwallettransaction(txid)
result = mc.listaddresstransactions(address) # 10 most recent
result = mc.listaddresstransactions(address, 10, 30) # paging backwards through transactions
result = mc.listwallettransactions() # 10 most recent
result = mc.listwallettransactions(10, 30) # paging backwards through transactions


################################
##  Sending one-way payments  ##
################################

# see online API documentation for native currency, multiple assets, inline metadata
txid = mc.send(address, {'asset1' : 20}) # one fungible asset
txid = mc.send(address, {'asset1' : {'token' : 'token1', 'qty' : 5}}) # non-fungible asset token
txid = mc.sendfrom(fromaddress, address, {'asset1' : 20})

txid = mc.sendasset(address, 'asset1', 20)
txid = mc.sendassetfrom(fromaddress, address, 'asset1', 20)

# see online API documentation for many more ways to attach data
txid = mc.sendwithdata(address, {'asset1' : 20}, 'a1b2c3d4') # raw binary data
txid = mc.sendwithdata(address, {'asset1' : 20}, {'for' : 'stream1', 'keys' : ['key1'], 'data' : {'json' : {'name' : 'Mary'}}}) # JSON stream item
txid = mc.sendwithdatafrom(fromaddress, address, {'asset1' : 20}, 'a1b2c3d4')


####################################
##  Atomic exchange transactions  ##
####################################

result = mc.appendrawexchange(txhex, txid, vout, {'asset1' : 10})
txhex = mc.completerawexchange(txhex_in, txid, vout, {'asset1' : 10})
txhex = mc.createrawexchange(txid, vout, {'asset1' : 10})
result = mc.decoderawexchange(txhex)

txid = mc.disablerawtransaction(txhex)

result = mc.preparelockunspent({'asset1' : 10})
result = mc.preparelockunspentfrom(fromaddress, {'asset1' : 10})


#########################
##  Stream management  ##
#########################

# see online API documentation for more options when creating a stream
txid = mc.create('stream', 'stream1', True) # open to all to write
txid = mc.create('stream', 'stream1', {'restrict' : 'write'}) # write-restricted
txid = mc.create('stream', 'stream1', {'restrict' : 'write,read'}) # read/write-restricted (requires Enterprise)
txid = mc.create('stream', 'stream1', False, {'purpose' : 'inventory'}) # custom fields
txid = mc.createfrom(fromaddress, 'stream', 'stream1', False)

result = mc.getstreaminfo('stream1')
result = mc.liststreams() # all streams
result = mc.liststreams('stream1') # one specific stream
result = mc.liststreams(['stream1', 'stream2']) # multiple specific streams
result = mc.liststreams('*', False, 10, 30) # paging through streams


###############################
##  Publishing stream items  ##
###############################

txid = mc.publish('stream1', 'key1', 'a1b2c3d4') # raw binary data
txid = mc.publish('stream1', 'key1', {'text' : 'hello world'}) # text data
txid = mc.publish('stream1', 'key1', {'json' : {'name' : 'John', 'age' : 30}}) # JSON data
txid = mc.publish('stream1', 'key1', {'cache' : 'Ev1HQV1aUCY'}) # data from binary cache
txid = mc.publish('stream1', ['key1', 'key2'], 'a1b2c3d4') # multiple keys
txid = mc.publish('stream1', 'key1', 'a1b2c3d4', 'offchain') # data offchain
txid = mc.publishfrom(fromaddress, 'stream1', 'key1', 'a1b2c3d4')

# see online API documentation for multi-publishing offchain
txid = mc.publishmulti('stream1', [
    {'key' : 'key1', 'data' : {'json' : {'name' : 'John', 'age' : 30}}},
    {'keys' : ['key2', 'key3'], 'data' : {'json' : {'name' : 'Iogan', 'age' : 20}}}
])
txid = mc.publishmultifrom(fromaddress, 'stream1', [
    {'key' : 'key1', 'data' : {'json' : {'name' : 'John', 'age' : 30}}},
    {'keys' : ['key2', 'key3'], 'data' : {'json' : {'name' : 'Iogan', 'age' : 20}}}
])


###############################################
##  Managing stream and asset subscriptions  ##
###############################################

# none of these commands return a result, check mc.success()
mc.subscribe('stream1') # one asset or stream
mc.subscribe(['stream1', 'asset1']) # multiple assets or streams
mc.subscribe('stream1', True, 'items,keys') # partial subscription (requires Enterprise)

mc.trimsubscribe('stream1', 'items-local,keys-local') # requires Enterprise
mc.unsubscribe('asset1')
mc.unsubscribe('stream1', True) # purge off-chain data


##################################
##  Querying subscribed assets  ##
##################################

result = mc.getassettransaction('asset1', txid)
result = mc.listassettransactions('asset1') # 10 most recent
result = mc.listassettransactions('asset1', False, 10, 30) # paging through transactions


###################################
##  Querying subscribed streams  ##
###################################

# see online API documentation for verbose, local ordering, more summarization options

result = mc.liststreamitems('stream1') # 10 most recent items
result = mc.liststreamitems('stream1', False, 10, 30) # paging through items
result = mc.liststreamkeyitems('stream1', 'key1') # 10 most recent key items
result = mc.liststreamkeyitems('stream1', 'key1', False, 10, 30) # paging through items
result = mc.liststreampublisheritems('stream1', address) # 10 most recent publisher items
result = mc.liststreampublisheritems('stream1', address, False, 10, 30) # paging through items

result = mc.liststreamkeys('stream1') # all keys in stream
result = mc.liststreamkeys('stream1', 'key1') # one specific keys
result = mc.liststreamkeys('stream1', ['key1', 'key2']) # multiple specific keys
result = mc.liststreamkeys('stream1', '*', False, 10, 30) # paging through keys
result = mc.liststreampublishers('stream1') # all publishers in stream
result = mc.liststreampublishers('stream1', address) # one specific publisher
result = mc.liststreampublishers('stream1', [address1, address2]) # multiple specific publishers
result = mc.liststreampublishers('stream1', '*', False, 10, 30) # paging through publishers

result = mc.liststreamblockitems('stream1', 1234) # one block
result = mc.liststreamblockitems('stream1', '1-100') # block range
result = mc.liststreamblockitems('stream1', -10) # most recent blocks
result = mc.liststreamblockitems('stream1',
    {'starttime' : 1577836800, 'endtime' : 1609459199}) # blocks stamped in time range

result = mc.getstreamkeysummary('stream1', 'key1', 'jsonobjectmerge')
result = mc.getstreampublishersummary('stream1', address, 'jsonobjectmerge,recursive')
result = mc.liststreamqueryitems('stream1', {'keys' : ['key1', 'key2']}) # items with both keys (AND logic)
result = mc.liststreamqueryitems('stream1', {'key' : 'key1', 'publisher' : address}) # with key and publisher

result = mc.getstreamitem('stream1', txid)
result = mc.liststreamtxitems('stream1', txid)

hex = mc.gettxoutdata(txid, vout) # all data
hex = mc.gettxoutdata(txid, vout, 1048576, 3145728) # paging within data


###################################################
##  Controlling offchain data (Enterprise only)  ##
###################################################

result = mc.purgepublisheditems('all') # all published data, use with extreme caution!
result = mc.purgepublisheditems(txid) # one specific transaction
result = mc.purgepublisheditems([txid1, txid2]) # multiple specific transactions
result = mc.purgepublisheditems({'blocks' : 1234}) # one specific block
result = mc.purgepublisheditems({'blocks' : '1-100'}) # block range
result = mc.purgepublisheditems({'blocks' :
    {'starttime' : 1577836800, 'endtime' : 1609459199}}) # blocks in time range

result = mc.purgestreamitems('stream1', 'all') # all retrieved data in stream
result = mc.purgestreamitems('stream1', txid) # one specific transaction
result = mc.purgestreamitems('stream1', [txid1, txid2]) # multiple specific transactions
result = mc.purgestreamitems('stream1', {'blocks' : 1234}) # one specific block
result = mc.purgestreamitems('stream1', {'blocks' : '1-100'}) # block range
result = mc.purgestreamitems('stream1', {'blocks' :
    {'starttime' : 1577836800, 'endtime' : 1609459199}}) # blocks in time range
result = mc.purgestreamitems('stream1', {'key' : 'key1'}) # one specific key
result = mc.purgestreamitems('stream1', {'keys' : ['key1', 'key2']}) # items with both keys (AND logic)
result = mc.purgestreamitems('stream1', {'publisher' : address}) # one specific publisher

result = mc.retrievestreamitems('stream1', 'all') # all unretrieved data in stream
result = mc.retrievestreamitems('stream1', txid) # one specific transaction
result = mc.retrievestreamitems('stream1', [txid1, txid2]) # multiple specific transactions
result = mc.retrievestreamitems('stream1', {'blocks' : 1234}) # one specific block
result = mc.retrievestreamitems('stream1', {'blocks' : '1-100'}) # block range
result = mc.retrievestreamitems('stream1', {'blocks' :
    {'starttime' : 1577836800, 'endtime' : 1609459199}}) # blocks in time range
result = mc.retrievestreamitems('stream1', {'key' : 'key1'}) # one specific key
result = mc.retrievestreamitems('stream1', {'keys' : ['key1', 'key2']}) # items with both keys (AND logic)
result = mc.retrievestreamitems('stream1', {'publisher' : address}) # one specific publisher


#######################################
##  Managing wallet unspent outputs  ##
#######################################

txids = mc.combineunspent() # see online API documentation for many more options

result = mc.listunspent()
result = mc.listunspent(0) # including unconfirmed transactions
result = mc.listunspent(1, 999999999, [address1, address2]) # specific addresses only

result = mc.listlockunspent()
result = mc.lockunspent(True) # unlock all outputs
result = mc.lockunspent(False, [{'txid' : txid, 'vout' : vout}]) # lock specific output
result = mc.lockunspent(True, [{'txid' : txid, 'vout' : vout}]) # unlock specific output


#####################################
##  Working with raw transactions  ##
#####################################

# the next four APIs accept a very large range of parameters for building transactions
# see online documentation, 'help addresses-all' and 'help data-all' inside multichain
# also see next section here for many examples using createrawsendfrom

txhex = mc.appendrawdata(txhex_in,
    {'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4'}
)

txhex = mc.appendrawtransaction(txhex_in,
    [{'txid' : txid1, 'vout' : vout1}, {'txid' : txid2, 'vout' : vout2}], # inputs to add
    {address1 : {'asset1' : 10}, address2 : {'asset2' : 20}}, # address-based outputs to add
    [{'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4'}], # data outputs to add
    'sign' # additional action to perform
)

txhex = mc.createrawtransaction(
    [{'txid' : txid1, 'vout' : vout1}, {'txid' : txid2, 'vout' : vout2}], # inputs to add
    {address1 : {'asset1' : 10}, address2 : {'asset2' : 20}}, # address-based outputs to add
    [{'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4'}], # data outputs to add
    'send' # additional action to perform
)

txhex = mc.createrawsendfrom(fromaddress,
    {address1 : {'asset1' : 10}, address2 : {'asset2' : 20}}, # address-based outputs to add
    [{'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4'}], # data outputs to add
    'send' # additional action to perform
)

txhex = mc.appendrawchange(txhex_in, address)
result = mc.decoderawtransaction(txhex)
txid = mc.sendrawtransaction(txhex)
result = mc.signrawtransaction(txhex)


#####################################
##  Examples of createrawsendfrom  ##
#####################################

# sending an empty transaction output (examples for action parameter)
txhex = mc.createrawsendfrom(fromaddress, {address : 0})
txhex = mc.createrawsendfrom(fromaddress, {address : 0}, [], 'lock') # also lock the inputs
result = mc.createrawsendfrom(fromaddress, {address : 0}, [], 'sign') # also sign the transaction
result = mc.createrawsendfrom(fromaddress, {address : 0}, [], 'lock,sign') # lock and sign
txid = mc.createrawsendfrom(fromaddress, {address : 0}, [], 'send') # sign and send (lock irrelevant)

# publishing stream item(s)
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4'}]) # raw binary data
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'for' : 'stream1', 'key' : 'key1', 'data' : {'text' : 'hello world'}}]) # text data
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'for' : 'stream1', 'key' : 'key1', 'data' : {'json' : {'name' : 'John', 'age' : 30}}}]) # JSON data
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'for' : 'stream1', 'key' : 'key1', 'data' : {'cache' : 'Ev1HQV1aUCY'}}]) # data from binary cache
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'for' : 'stream1', 'keys' : ['key1', 'key2'], 'data' : 'a1b2c3d4'}]) # multiple keys
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4', 'options' : 'offchain'}]) # data offchain
txhex = mc.createrawsendfrom(fromaddress, {}, [
    {'for' : 'stream1', 'key' : 'key1', 'data' : 'a1b2c3d4'},
    {'for' : 'stream2', 'key' : 'key2', 'data' : {'text' : 'hello world'}}
]) # multiple items

# sending native currency, asset(s), token(s)
txhex = mc.createrawsendfrom(fromaddress, {address : 1.0}) # native currency
txhex = mc.createrawsendfrom(fromaddress, {address : {'asset1' : 10}}) # asset
txhex = mc.createrawsendfrom(fromaddress,
    {address1 : {'asset1' : 100}, address2 : {'asset1' : 10}}) # asset to two addresses
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'nfts1' : {'token' : 'token1', 'qty' : 1}}}) # token
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'nfts1' : [{'token' : 'token1', 'qty' : 1}, {'token' : 'token2', 'qty' : 1}]}}) # two tokens

# sending asset or token with metadata
txhex = mc.createrawsendfrom(fromaddress, {address : {'asset1' : 10}},
    ['a1c3b245d37e']) # asset with raw binary metadata
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'nfts1' : {'token' : 'token1', 'qty' : 1}}},
    [{'for' : 'stream1', 'key' : 'key1', 'data' : {'json' : {'name' : 'John'}}}]
) # token with JSON stream item

# creating a stream - see 'help data-all' in multichain for more options
txhex = mc.createrawsendfrom(fromaddress, {}, [{'create' : 'stream', 'name' : 'stream1'}])
txhex = mc.createrawsendfrom(fromaddress, {}, [{
    'create' : 'stream', 'name' : 'stream1', 'restrict' : 'read,write',
    'details' : {'purpose' : 'inventory'}
}])

# issuing assets - see 'help addresses-all' and 'help data-all' in multichain for more options
txhex = mc.createrawsendfrom(fromaddress, {address : {'issue' : {'raw' : 100000}}},
    [{'create' : 'asset', 'name' : 'asset1', 'multiple' : 100, 'open' : True}]) # issue fungible asset
txhex = mc.createrawsendfrom(fromaddress, {address : {'issue' : {'raw' : 0}}},
    [{'create' : 'asset', 'name' : 'nfts1', 'open' : True, 'fungible' : False}]) # issue non-fungible asset
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'issuemore' : {'asset' : 'asset1', 'raw' : 1000}}}) # issue more of fungible asset
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'issuetoken' : {'asset' : 'nfts1', 'raw' : 1, 'token' : 'token1'}}}) # issue non-fungible token
txhex = mc.createrawsendfrom(fromaddress, {'asset1' : {'open' : True}}) # change asset openness

# setting permissions
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'permissions' : {'type' : 'send,receive'}}}) # global permission grant
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'permissions' : {'type' : 'send,receive', 'startblock' : 0, 'endblock' : 0}}}) # global permission revoke
txhex = mc.createrawsendfrom(fromaddress,
    {address : {'permissions' : {'for' : 'stream1', 'type' : 'write'}}}) # per-entity permission grant

# creating and approving filters and upgrades
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'create' : 'txfilter', 'name' : 'txfilter1', 'code' : 'function filtertransaction() {}'}]) # create tx filter
txhex = mc.createrawsendfrom(fromaddress,
    {'txfilter1' : {'approve' : True}}) # approve tx filter
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'create' : 'streamfilter', 'name' : 'streamfilter1', 'code' : 'function filterstreamitem() {}'}]) # create stream filter
txhex = mc.createrawsendfrom(fromaddress,
    {'streamfilter1' : {'approve' : True, 'for' : 'stream1'}}) # approve stream filter
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'create' : 'upgrade', 'name' : 'upgrade1', 'details' : {'protocol-version' : 20013}}])  # create upgrade
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'approve' : True, 'for' : 'upgrade1'}]) # approve upgrade

# creating and updating variables
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'create' : 'variable', 'name' : 'var1'}]) # create variable
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'create' : 'variable', 'name' : 'var1', 'value' : 'london'}]) # create variable with default value
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'update' : 'var1', 'value' : 'new york'}]) # update variable value

# creating, updating, approving updates for libraries
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'create' : 'library', 'name' : 'lib1', 'updatemode' : 'approve', 'code' : 'function f1() {}'}]) # create library
txhex = mc.createrawsendfrom(fromaddress, {},
    [{'update' : 'lib1', 'updatename' : 'lib1_2', 'code' : 'function f1() {}'}]) # update library code
txhex = mc.createrawsendfrom(fromaddress,
    {'lib1' : {'approve' : True, 'updatename' : 'lib1_2'}}) # approve library update


################################
##  Peer-to-peer connections  ##
################################

mc.addnode('12.34.56.78', 'add') # no result, check mc.success()
result = mc.getaddednodeinfo(True) # all added nodes
result = mc.getaddednodeinfo(True, '12.34.56.78') # one added node

mc.storenode('12.34.56.78') # no result, check mc.success()
mc.storenode('12.34.56.78', 'ignore') # no result, check mc.success()
result = mc.liststorednodes()

result = mc.getnetworkinfo()
result = mc.getpeerinfo()
mc.ping() # no result, check mc.success()


##########################################
##  Messaging signing and verification  ##
##########################################

signature = mc.signmessage(address, 'It is my message')
result = mc.verifymessage(address, signature, 'It is my message')


###############################
##  Querying the blockchain  ##
###############################

result = mc.getblock(1) # by height
result = mc.getblock(hash) # by block hash
result = mc.getblock(1, 4) # highest level of verbosity
result = mc.getblockhash(1)
result = mc.getlastblockinfo() # most recent block
result = mc.getlastblockinfo(10) # 10 blocks before most recent

result = mc.listblocks(1234) # one block by height
result = mc.listblocks(hash) # one block by hash
result = mc.listblocks([hash1, hash2]) # multiple blocks by hash
result = mc.listblocks('1-100') # block range
result = mc.listblocks(-10) # most recent blocks
result = mc.listblocks({'starttime' : 1577836800, 'endtime' : 1609459199}) # blocks stamped in time range

result = mc.getblockchaininfo()
result = mc.getchaintotals()
result = mc.getmempoolinfo()
result = mc.getrawmempool()
result = mc.listminers()

txhex = mc.getrawtransaction(txid) # get transaction as hex
result = mc.getrawtransaction(txid, True) # get transaction description
result = mc.gettxout(txid1, vout)


####################
##  Binary cache  ##
####################

cacheid = mc.createbinarycache()
size = mc.appendbinarycache(cacheid, '') # query length
size = mc.appendbinarycache(cacheid, 'a1b2c3d4') # append data
mc.deletebinarycache(cacheid) # no result, check mc.success()
size = mc.txouttobinarycache(cacheid, txid, vout) # all data
size = mc.txouttobinarycache(cacheid, txid, vout, 1048576, 3145728) # paging within data


###############################
##  Advanced wallet control  ##
###############################

# encryptwallet and walletpassphrasechange omitted
mc.backupwallet('/path/to/wallet.dat.bak') # no result, check mc.success()
privkey = mc.dumpprivkey(address)
mc.dumpwallet('/path/to/wallet.txt') # no result, check mc.success()
result = mc.getwalletinfo()
mc.importprivkey(privkey) # no result, check mc.success()
result = mc.importwallet('/path/to/wallet.txt') # no result, check mc.success()
mc.walletlock() # no result, check mc.success()
mc.walletpassphrase('mypassword', 60) # no result, check mc.success()


############################################
##  Working with feeds (Enterprise only)  ##
############################################

mc.addtofeed('feed1', 'stream1') # no result, check mc.success()
mc.createfeed('feed1') # no result, check mc.success()
mc.deletefeed('feed1') # no result, check mc.success()
result = mc.listfeeds()
mc.pausefeed('feed1') # no result, check mc.success()
mc.purgefeed('feed1', -30) # older than 30 days, no result, check mc.success()
mc.resumefeed('feed1') # no result, check mc.success()
mc.updatefeed('feed1', ['stream1', 'stream2'], '*', 'sync') # no result, check mc.success()

size = mc.datareftobinarycache(cacheid, dataref) # all data
size = mc.datareftobinarycache(cacheid, dataref, 1048576, 3145728) # paging within data
hex = mc.getdatarefdata(dataref) # all data
hex = mc.getdatarefdata(dataref, 1048576, 3145728) # paging within data


##################################
##  Smart filters and upgrades  ##
##################################

txid = mc.approvefrom(fromaddress, 'txfilter1', True) # approve tx filter
txid = mc.approvefrom(fromaddress, 'upgrade1', True) # approve upgrade
txid = mc.approvefrom(fromaddress, 'streamfilter1',
    {'for' : 'stream1', 'approve' : True}) # approve stream filter

txid = mc.create('streamfilter', 'streamfilter1', {},
    'function filterstreamitem() {}') # create stream filter
txid = mc.create('streamfilter', 'streamfilter1', {'libraries' : ['lib1', 'lib2']},
    'function filterstreamitem() {}') # create stream filter that uses libraries
txid = mc.createfrom(fromaddress, 'streamfilter', 'streamfilter1', {},
    'function filterstreamitem() {}') # create stream filter from specific address

txid = mc.create('txfilter', 'txfilter1', {},
    'function filtertransaction() {}') # create tx filter
txid = mc.create('txfilter', 'txfilter1', {'libraries' : ['lib1', 'lib2']},
    'function filtertransaction() {}') # create tx filter that uses libraries
txid = mc.create('txfilter', 'txfilter1', {'for' : 'asset1'},
    'function filtertransaction() {}') # create tx filter active for one entity only
txid = mc.create('txfilter', 'txfilter1', {'for' : ['asset1', 'asset2']},
    'function filtertransaction() {}') # create tx filter active for specific entities only
txid = mc.createfrom(fromaddress, 'txfilter', 'txfilter1', {},
    'function filtertransaction() {}') # create tx filter from specific address

txid = mc.create('upgrade', 'upgrade1', False,
    {'protocol-version' : 20013, 'maximum-block-size' : 16777216}) # create upgrade
txid = mc.createfrom(fromaddress, 'upgrade', 'upgrade1', False,
    {'protocol-version' : 20013, 'maximum-block-size' : 16777216}) # create upgrade from specific address

code = mc.getfiltercode('filter1')

result = mc.liststreamfilters() # all stream filters
result = mc.liststreamfilters('streamfilter1') # one specific stream filter
result = mc.liststreamfilters(['streamfilter1', 'streamfilter2']) # multiple specific stream filters

result = mc.listtxfilters() # all tx filters
result = mc.listtxfilters('txfilter1') # one specific tx filter
result = mc.listtxfilters(['txfilter1', 'txfilter2']) # multiple specific tx filters

result = mc.listupgrades() # all upgrades
result = mc.listupgrades('upgrade1') # one specific upgrade
result = mc.listupgrades(['upgrade1', 'upgrade2']) # multiple specific upgrades

result = mc.runstreamfilter('streamfilter1', txhex) # test on transaction hex
result = mc.runstreamfilter('streamfilter1', txid) # test on previous transaction

result = mc.teststreamfilter({}, 'function filterstreamitem() {}') # compile test only
result = mc.teststreamfilter({'libraries' : ['lib1', 'lib2']}, 'function filterstreamitem() {}') # with libraries
result = mc.teststreamfilter({}, 'function filterstreamitem() {}', txhex) # test on transaction hex
result = mc.teststreamfilter({}, 'function filterstreamitem() {}', txid) # test on previous transaction

result = mc.runtxfilter('txfilter1', txhex) # test on transaction hex
result = mc.runtxfilter('txfilter1', txid) # test on previous transaction

result = mc.testtxfilter({}, 'function filtertransaction() {}') # compile test only
result = mc.testtxfilter({'libraries' : ['lib1', 'lib2']}, 'function filtertransaction() {}') # with libraries
result = mc.testtxfilter({'for' : 'asset1'}, 'function filtertransaction() {}') # active for one entity only
result = mc.testtxfilter({}, 'function filtertransaction() {}', txhex) # test on transaction hex
result = mc.testtxfilter({}, 'function filtertransaction() {}', txid) # test on previous transaction


#############################
## Libraries and variables ##
#############################

txid = mc.addlibraryupdate('lib1', 'lib1_2', 'function f1() {}')
txid = mc.addlibraryupdatefrom(fromaddress, 'lib1', 'lib1_2', 'function f1() {}')
txid = mc.approvefrom(fromaddress, 'lib1', {'updatename' : 'lib1_2', 'approve' : True})

txid = mc.create('library', 'lib1', {'updatemode' : 'approve'}, 'function f1() {}')
txid = mc.createfrom(fromaddress, 'library', 'lib1', {'updatemode' : 'approve'}, 'function f1() {}')

code = mc.getlibrarycode('lib1') # currently active code
code = mc.getlibrarycode('lib1', '') # original code before updates
code = mc.getlibrarycode('lib1', 'lib1_2') # specific update name

result = mc.listlibraries() # all libraries
result = mc.listlibraries('lib1') # one specific library
result = mc.listlibraries(['lib1', 'lib2']) # multiple specific libraries

result = mc.testlibrary() # get information on test libraries
result = mc.testlibrary('libtemp', '', 'function f1() {}') # create new test library
result = mc.testlibrary('libtemp', 'libtemp_2', 'function f1() {}') # create test library update
result = mc.testlibrary('libtemp', 'libtemp_2') # switch to previous update of test library
result = mc.testlibrary('libtemp') # clear code for this test library
result = mc.testlibrary('*') # clear code for all test libraries

txid = mc.create('variable', 'var1') # no default value
txid = mc.create('variable', 'var1', True, 'tokyo') # with default value
txid = mc.createfrom(fromaddress, 'variable', 'var1') # no default value
txid = mc.createfrom(fromaddress, 'variable', 'var1', True, 'tokyo') # with default value

result = mc.getvariablehistory('var1') # entire history
result = mc.getvariablehistory('var1', False, 10, 30) # paging through history
result = mc.getvariableinfo('var1')
value = mc.getvariablevalue('var1')

result = mc.listvariables() # all variables
result = mc.listvariables('var1') # one specific variable
result = mc.listvariables(['var1', 'var2']) # multiple specific variables
result = mc.listvariables('*', False, 10, 30) # paging through variables

txid = mc.setvariablevalue('var1') # clear value (set to null)
txid = mc.setvariablevalue('var1', 1234) # set value to number
txid = mc.setvariablevalue('var1', 'toronto') # set value to string
txid = mc.setvariablevalue('var1', {'a' : 1, 'b' : 2}) # set value to JSON structure
txid = mc.setvariablevaluefrom(fromaddress, 'var1') # clear value (set to null)
txid = mc.setvariablevaluefrom(fromaddress, 'var1', 1234) # set value


#############################
##  Advanced node control  ##
#############################

mc.clearmempool() # no result, check mc.success()
result = mc.getchunkqueueinfo()
result = mc.getchunkqueuetotals()
mc.pause('incoming,mining') # no result, check mc.success()
mc.resume('incoming,mining') # no result, check mc.success()
hash = mc.setlastblock(hash) # by block hash
hash = mc.setlastblock(1234) # by block height


#######################################
##  MultiChain Enterprise licensing  ##
#######################################

hex = mc.getlicenserequest()
txid = mc.activatelicense(hex)
result = mc.listlicenses() # all licenses
result = mc.listlicenses('license-a1b2-c3d4-e5f6-7890') # one specific license
result = mc.listlicenses([license1, license2]) # multiple specific licenses
txid = mc.transferlicense('license-a1b2-c3d4-e5f6-7890', hex)
