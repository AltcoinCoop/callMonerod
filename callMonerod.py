#!/usr/bin/env python

import requests
import json

hdr = {'content-type':'application/json'}
monerod = "http://localhost:18081/"


def call_jsonrpc( f ):
    def req( *args ):
        jsonCall = f( *args )
        r = requests.post( monerod + "json_rpc", data=f( *args ), headers = hdr )
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
        

def wrap_and_call_rpc( f ):
    def message( *args ):
        command = f( *args )
        resource = command[0]
        if len( command[1] ) > 0:
            r = requests.post( monerod + resource, data=json.dumps( command[1] ), headers = hdr )
        else:
            r = requests.post( monerod + resource, headers = hdr )
        if r.status_code != 200:
            return "Some error occured"
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            return r.text


        return json.dumps( result, indent = 4 )
    return message

def wrap_to_json_rpc( f ):
    def message( *args ):
        command = f( *args )
        payload = { "id": "0", "jsonrpc": "2.0", "method": command[0] }
        if len( command[1] ) > 0:
            payload["params"] = command[1]
        return json.dumps( payload, indent=4 )
    return message


@call_jsonrpc
@wrap_to_json_rpc
def getblockcount():
    return [ "getblockcount", dict() ]

@call_jsonrpc
@wrap_to_json_rpc
def on_getblockhash( height ):
    return [ "on_getblockhash", [ height ] ]

@call_jsonrpc
@wrap_to_json_rpc
def getblocktemplate( address, reserve_size ):
    return [ "getblocktemplate", {"wallet_address": address, "reserve_size": reserve_size} ]

@call_jsonrpc
@wrap_to_json_rpc
def submitblock( blockHex ):
    return [ "submitblock", [blockHex] ]

@call_jsonrpc
@wrap_to_json_rpc
def getlastblockheader():
    return [ "getlastblockheader", dict() ]

@call_jsonrpc
@wrap_to_json_rpc
def getblockheaderbyhash( height ):
    return [ "getblockheaderbyhash", {"hash": height} ]

@call_jsonrpc
@wrap_to_json_rpc
def getblockheaderbyheight( height ):
    return [ "getblockheaderbyheight", {"height": height} ]

@call_jsonrpc
@wrap_to_json_rpc
def getblock( heightOrHash ):
    if type( heightOrHash ) == int:
        paramname = "height"
    else:
        paramname = "hash"
    return [ "getblock", { paramname: heightOrHash } ]

@call_jsonrpc
@wrap_to_json_rpc
def get_connections():
    return [ "get_connections", dict() ]

@call_jsonrpc
@wrap_to_json_rpc
def get_info():
    return [ "get_info", dict() ]

@call_jsonrpc
@wrap_to_json_rpc
def hard_fork_info():
    return [ "hard_fork_info", dict() ]

@call_jsonrpc
@wrap_to_json_rpc
def set_bans( banlist ):
    return [ "set_bans", { "bans":[{"ip":i[0], "ban": i[1], "seconds": i[2]} for i in banlist]} ]

@call_jsonrpc
@wrap_to_json_rpc
def get_bans():
    return [ "get_bans", dict() ]

########################################################################
###          other RPC methods

@wrap_and_call_rpc
def getheight():
    return ["getheight", dict() ]

@wrap_and_call_rpc
def gettransactions( hashlist, decode_as_json = True ):
    return ["gettransactions", {"txs_hashes": hashlist, "decode_as_json": decode_as_json} ]

@wrap_and_call_rpc
def is_key_image_spent( key_img_list ):
    return ["is_key_image_spent", { "key_imgages": key_img_list } ]

@wrap_and_call_rpc
def sendrawtransaction( hash ):
    return ["sendrawtransaction", {"tx_as_hex": hash} ]

@wrap_and_call_rpc
def get_transaction_pool():
    return ["get_transaction_pool", dict() ]

@wrap_and_call_rpc
def stop_daemon():
    return ["stop_daemon", dict() ]


#json-rpc calls

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


#### other rpc calls

#print( getheight() )
#print( gettransactions( ["11c7871239322547156db5ffe556edbde4b915fc6ca701a0fac9a3256a3c3733", "9670f03031541be633c3781d00eb69ee8774e4d079c17a5fb132bf4c83c061fb"] ) )
#print( is_key_image_spent( ["8d1bd8181bf7d857bdb281e0153d84cd55a3fcaa57c3e570f4a49f935850b5e3", "7319134bfc50668251f5b899c66b005805ee255c136f0e1cecbb0f3a912e09d4"] ) )
#print( sendrawtransaction( "510ee3c4e14330a7b96e883c323a60ebd1b5556ac1262d0bc03c24a3b785516f" ) )
#print( get_transaction_pool() )
#print( stop_daemon() )
