import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi { abi from meta mask deployed abi }
abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "_favoriteNumber",
                                "type": "uint256"
            }
        ],
        "name": "addPerson",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_favoriteNumber",
                                "type": "uint256"
            }
        ],
        "name": "store",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                                "type": "string"
            }
        ],
        "name": "nameToFavoriteNumber",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                                "type": "uint256"
            }
        ],
        "name": "people",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "favoriteNumber",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "retrieve",
                "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider(
    "https://polygon-mumbai.g.alchemy.com/v2/K59YdNGK95akCLJrA1m9nYPZ7JYNa8Me"))  # alchemy HTTP link
chain_id = 80001  # polygon-mumbai chain id

if chain_id == 4:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.clientVersion)
# Added print statement to ensure connection suceeded as per
# https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority

my_address = "0x042bDdB896fa2B4F5993e3926b7dD53B27f9321E"  # --My metamask id


# --my private account { metamask => settings => Accounts detials => Export private key }
private_key = "0x6021d22205954e378994c07b70dae0afd8e67b5eb61c8f799ebfd24f5f010708"

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End Deployment >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ----------------------------------------------- Create obj forf contract --------------------------------------------------------

# Working with deployed Contracts
simple_storage = w3.eth.contract(
    address='0x52B4100E9474f731C67f43E5C0A24Db756De6c4A', abi=abi)  # the contract deployed from metamask

# ---------------------------------------------------------------------------------------------------------------------------------

print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

tx_greeting_hash = w3.eth.send_raw_transaction(
    signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Next value >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


greeting_transaction = simple_storage.functions.store(2).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 2,
    }
)

signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

tx_greeting_hash = w3.eth.send_raw_transaction(
    signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
