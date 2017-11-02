#!/usr/bin/env python

import requests
import json

monerod = "http://localhost:18081/json_rpc"
hdr = {'content-type':'application/json'}

#x = json.dumps(hdr)

def callMonerod( f ):
    def req( *args ):
        jsonCall = f( *args )
        r = requests.post( monerod, data=f( *args ), headers = hdr )
        #return json.dumps( r.json(), indent=4 )
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            return r.text
        if "error" in result:
            return "Error: " + result["error"]["message"]
        elif "result" in result:
            return json.dumps( result["result"], indent = 4 )
        else:
            return "Some other error"
    return req
        

def rpcMessage( f ):
    def message( *args ):
        command = f( *args )
        payload = { "id": "0", "jsonrpc": "2.0", "method": command[0] }
        if len( command[1] ) > 0:
            payload["params"] = command[1]
        return json.dumps( payload, indent=4 )
    return message


@callMonerod
@rpcMessage
def getblockcount():
    return [ "getblockcount", dict() ]

@callMonerod
@rpcMessage
def on_getblockhash( height ):
    return [ "on_getblockhash", [ height ] ]

@callMonerod
@rpcMessage
def getblocktemplate( address, reserve_size ):
    return [ "getblocktemplate", {"wallet_address": address, "reserve_size": reserve_size} ]

@callMonerod
@rpcMessage
def submitblock( blockHex ):
    return [ "submitblock", [blockHex] ]

@callMonerod
@rpcMessage
def getlastblockheader():
    return [ "getlastblockheader", dict() ]

@callMonerod
@rpcMessage
def getblockheaderbyhash( height ):
    return [ "getblockheaderbyhash", {"hash": height} ]

@callMonerod
@rpcMessage
def getblockheaderbyheight( height ):
    return [ "getblockheaderbyheight", {"height": height} ]

@callMonerod
@rpcMessage
def getblock( heightOrHash ):
    if type( heightOrHash ) == int:
        paramname = "height"
    else:
        paramname = "hash"
    return [ "getblock", { paramname: heightOrHash } ]

@callMonerod
@rpcMessage
def get_connections():
    return [ "get_connections", dict() ]

@callMonerod
@rpcMessage
def get_info():
    return [ "get_info", dict() ]

@callMonerod
@rpcMessage
def hard_fork_info():
    return [ "hard_fork_info", dict() ]

@callMonerod
@rpcMessage
def set_bans( banlist ):
    return [ "set_bans", { "bans":[{"ip":i[0], "ban": i[1], "seconds": i[2]} for i in banlist]} ]

@callMonerod
@rpcMessage
def get_bans():
    return [ "get_bans", dict() ]


#print( getblockcount() )
#print( on_getblockhash( 1000000 ) )
#print( getblocktemplate("4549pSsbeKdWP8GrbBNAzYaAJvei3GNqrDyve3on3BtThciZQMfgGCTERrZTih6RFiUmKKe9rjtNz6BV2kHhLjM5JyxR4wv", 60) )
#print( submitblock("0606c8b3eecf05356c1fa701edd3067e6dcbe18c21e801ca8263554816ae670f4bd553e392ebe80000000002d4c65701ff98c657018af0e7a9e4af0102bbae42c97ce39be557dc4f3117b5a8ecc333c249750c8c920e07c34331b8f6f25f0167a6671e4a66b075f0d7a7a64a7f37e46c486cb0e43928fea59681da32a80d60023c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003893826a1bbb041fcdca8b3fdbf177e747106bc35785d96cb8fe27a4d5a5bd7c4d41316097cf19a5e728d7cc3b832b9d51a66afd3e2689bc43371556e1a0c0f200f137a4f20c0c70ee70fa780f144380e9ad78051d66f1246091f75990c004467") )
#print( getlastblockheader() )
#print( getblockheaderbyhash( "510ee3c4e14330a7b96e883c323a60ebd1b5556ac1262d0bc03c24a3b785516f") )
#print( getblockheaderbyheight(123) )
#print( getblock("510ee3c4e14330a7b96e883c323a60ebd1b5556ac1262d0bc03c24a3b785516f") )
#print( get_connections() )
#print( get_info() )
#print( hard_fork_info() )
#print( set_bans( [(838969536, True, 30), (838969535, True, 30) ] ) )
#print( get_bans() )
