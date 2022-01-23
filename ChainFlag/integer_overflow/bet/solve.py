from web3 import Web3, Account
from solcx import compile_files
from eth_tester import PyEVMBackend
import web3
import eth_abi
import rlp
import eth_keys
import random
import time

################################################################################
#              ______ _______ _    _            _   _ _                        #  
#             |  ____|__   __| |  | |          | | (_) |                       # 
#             | |__     | |  | |__| |     _   _| |_ _| |___                    #
#             |  __|    | |  |  __  |    | | | | __| | / __|                   # 
#             | |____   | |  | |  | |    | |_| | |_| | \__ \                   #   
#             |______|  |_|  |_|  |_|     \__,_|\__|_|_|___/                   #   
#                                                                              # 
#        A collection of helper for every-day ETH CTF challenges.              # 
################################################################################
                                            
################################################################################
#                             CONFIGURATION                                    #
################################################################################

# Set to
IS_TEST = False 

# Select RPC provider
if IS_TEST:
    RPC = "http://localhost:8545/"
    ARCHIVE_URL = "https://eth-ropsten.alchemyapi.io/v2/*******************"
    BLOCK_NUMBER = 11857541
    TEST_BALANCE = Web3.toWei(1, 'ether')
else:
    RPC = "https://eth-ropsten.alchemyapi.io/v2/****************************"

################################################################################
#                                UTILS                                         #
################################################################################

def mk_contract_address(sender, nonce):
    return Web3.sha3(rlp.encode([Web3.toBytes(hexstr=sender), nonce]))[12:]

def mk_selector(func):
    return Web3.keccak(text=func)[:4]

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
    global _chain_ids_cache

    if 'from' not in tx:
        tx['from'] = account.address

    if 'value' not in tx:
        tx['value'] = 0

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

    if 'gas' not in tx:
        tx['gas'] = int(w3.eth.estimate_gas(tx) * 1.03)

    if 'gas' not in tx:
        try:
            tx['gas'] = int(w3.eth.estimate_gas(tx) * 1.03)
        except:
            if IS_TEST:
                tx['gas'] = 100000
            else:
                raise RuntimeError("Cannot estimate gas (this can happen e.g. for variable size   operations)")

    signed = Account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def normalize_addr(address):
    if not isinstance(address, bytes):
        address = Web3.toBytes(hexstr=address)
    return address

def w3_is_test(w3):
    return isinstance(w3.provider, Web3.EthereumTesterProvider)

def w3_get_vm(w3):
    if not w3_is_test(w3):
        raise ValueError("Cannot get VM from non-test W3 instance")
    return w3.provider.ethereum_tester.backend.chain.get_vm()

def get_storage(w3, addr, slot):
    addr = normalize_addr(addr)
    if w3_is_test(w3):
        # https://github.com/ethereum/web3.py/issues/1490
        return w3_get_vm(w3).state.get_storage(addr, slot)
    else:
        return w3.eth.get_storage_at(addr,slot)

def set_storage(w3, addr, slot, val):
    if not w3_is_test(w3):
        raise ValueError("Cannot set storage of a non-test W3 instance")
    addr = normalize_addr(addr)
    w3_get_vm(w3).state.set_storage(addr, slot, val)

def get_mapping_slot(addr_sender, slot):
    # Encode address
    addr_sender = normalize_addr(addr_sender)
    addr_sender = eth_abi.encode_single('address', addr_sender)

    # Encode slot
    slot = eth_abi.encode_single('uint256', slot)

    # Concat and hash to get the storage slot
    keccak_hash = Web3.keccak(addr_sender + slot)
    return Web3.toInt(keccak_hash)

def get_mapping_storage(w3, addr_contract, addr_sender, slot):
    slot = get_mapping_slot(addr_sender, slot)
    return get_storage(addr_contract, slot)

################################################################################
# Your code starts here. To make things easier I added some boilerplate.       #
################################################################################

# Get web3 instance
w3 = Web3(Web3.HTTPProvider(RPC))

# Patch eth_maxPriorityFeePerGas, often not supported
web3.eth.Eth.max_priority_fee = get_max_priority_fee(w3)

# Get an account
account = Account.create()
account = Account.from_key(Web3.toBytes(hexstr="*********************************************"))

# Setup environment
if IS_TEST:
    w3.provider.make_request('hardhat_reset',
        # Don't forget to set the block number to your needs
        [{'forking': {'jsonRpcUrl': ARCHIVE_URL, 'blockNumber': BLOCK_NUMBER}}] 
    )
    #w3.provider.make_request('hardhat_setBalance',
    #    [account.address, hex(TEST_BALANCE)]
    #)
else:
    # Non-test setup
    pass

print(f"Balance {account.address}: {w3.eth.get_balance(account.address)}")

TARGET = Web3.toChecksumAddress("0x30d0a604d8c90064a0a3ca4beeea177eff3e9bcd")

# Boilerplate code to deploy a contract
compiled = compile_files(["Hack.sol"], output_values=["abi", "bin"], base_path=".", allow_paths=["../.."])['Hack.sol:Hack']
Hack = w3.eth.contract(abi=compiled['abi'], bytecode=compiled['bin'])
tx = Hack.constructor(TARGET).buildTransaction({
    'from': account.address,
})
tx_receipt = sign_and_send_transaction(w3, account, tx)
print(tx_receipt)









