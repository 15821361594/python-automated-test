from __future__ import print_function
from solc import *
from solc.exceptions import SolcError
from testrpc.client import EthTesterClient
from testrpc.client.utils import encode_data
from testrpc.client.utils import decode_hex
from ethereum.utils import sha3
from rlp.utils import big_endian_to_int

def fid(functionDef):
    end = functionDef.find("(")
    return functionDef[:end]

def test(contract, optimize):
    client = EthTesterClient()
    a = client.get_accounts()[0]
    try:
        bin = compile_source(contract,optimize=optimize).values()[0]['bin']
    except SolcError as e:
        print ("COMPILATION ERROR:")
        print (e)
        return "COMPILE ERROR"
    txnHash = client.send_transaction(_from = a, data = bytes(bin), value = 1234)
    txnReceipt = client.get_transaction(txnHash)
    contractAddress = txnReceipt['contractAddress']
    fsig = encode_data(sha3("f()")[:4])
    val = client.call(_from = a, to = contractAddress, data = fsig)
    return big_endian_to_int(decode_hex(val))

def differentialTest(functions):
    print ("TESTING:")
    print (functions)
    # Expects to receive a set of function definitions with a top-level, no-parameter, function called f()
    contract = "contract c {" + functions + "}"
    resultOpt = test(contract, True)
    resultNoOpt = test(contract, False)
    if resultOpt != resultNoOpt:
        print ("*"*80)
        print ("MISMATCH:")
        print ("CONTRACT:")
        print (contract)
        print ("="*50)
        print ("OPTIMIZED VALUE:", resultOpt)
        print ("="*50)        
        print ("NON-OPTIMIZED VALUE:",resultNoOpt)
        print ("*"*80)        
        assert False