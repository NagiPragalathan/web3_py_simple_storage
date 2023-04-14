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
bytecode = "608060405234801561001057600080fd5b5061093b806100206000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c80632e64cec11461005c5780636057361d1461007a5780636f760f41146100965780638bab8dd5146100b25780639e7a13ad146100e2575b600080fd5b610064610113565b60405161007191906102b2565b60405180910390f35b610094600480360381019061008f919061030d565b61011c565b005b6100b060048036038101906100ab9190610480565b610126565b005b6100cc60048036038101906100c791906104dc565b6101af565b6040516100d991906102b2565b60405180910390f35b6100fc60048036038101906100f7919061030d565b6101dd565b60405161010a9291906105a4565b60405180910390f35b60008054905090565b8060008190555050565b6001604051806040016040528083815260200184815250908060018154018082558091505060019003906000526020600020906002020160009091909190915060008201518160000155602082015181600101908161018591906107e0565b5050508060028360405161019991906108ee565b9081526020016040518091039020819055505050565b6002818051602081018201805184825260208301602085012081835280955050505050506000915090505481565b600181815481106101ed57600080fd5b906000526020600020906002020160009150905080600001549080600101805461021690610603565b80601f016020809104026020016040519081016040528092919081815260200182805461024290610603565b801561028f5780601f106102645761010080835404028352916020019161028f565b820191906000526020600020905b81548152906001019060200180831161027257829003601f168201915b5050505050905082565b6000819050919050565b6102ac81610299565b82525050565b60006020820190506102c760008301846102a3565b92915050565b6000604051905090565b600080fd5b600080fd5b6102ea81610299565b81146102f557600080fd5b50565b600081359050610307816102e1565b92915050565b600060208284031215610323576103226102d7565b5b6000610331848285016102f8565b91505092915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b61038d82610344565b810181811067ffffffffffffffff821117156103ac576103ab610355565b5b80604052505050565b60006103bf6102cd565b90506103cb8282610384565b919050565b600067ffffffffffffffff8211156103eb576103ea610355565b5b6103f482610344565b9050602081019050919050565b82818337600083830152505050565b600061042361041e846103d0565b6103b5565b90508281526020810184848401111561043f5761043e61033f565b5b61044a848285610401565b509392505050565b600082601f8301126104675761046661033a565b5b8135610477848260208601610410565b91505092915050565b60008060408385031215610497576104966102d7565b5b600083013567ffffffffffffffff8111156104b5576104b46102dc565b5b6104c185828601610452565b92505060206104d2858286016102f8565b9150509250929050565b6000602082840312156104f2576104f16102d7565b5b600082013567ffffffffffffffff8111156105105761050f6102dc565b5b61051c84828501610452565b91505092915050565b600081519050919050565b600082825260208201905092915050565b60005b8381101561055f578082015181840152602081019050610544565b60008484015250505050565b600061057682610525565b6105808185610530565b9350610590818560208601610541565b61059981610344565b840191505092915050565b60006040820190506105b960008301856102a3565b81810360208301526105cb818461056b565b90509392505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000600282049050600182168061061b57607f821691505b60208210810361062e5761062d6105d4565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026106967fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82610659565b6106a08683610659565b95508019841693508086168417925050509392505050565b6000819050919050565b60006106dd6106d86106d384610299565b6106b8565b610299565b9050919050565b6000819050919050565b6106f7836106c2565b61070b610703826106e4565b848454610666565b825550505050565b600090565b610720610713565b61072b8184846106ee565b505050565b5b8181101561074f57610744600082610718565b600181019050610731565b5050565b601f8211156107945761076581610634565b61076e84610649565b8101602085101561077d578190505b61079161078985610649565b830182610730565b50505b505050565b600082821c905092915050565b60006107b760001984600802610799565b1980831691505092915050565b60006107d083836107a6565b9150826002028217905092915050565b6107e982610525565b67ffffffffffffffff81111561080257610801610355565b5b61080c8254610603565b610817828285610753565b600060209050601f83116001811461084a5760008415610838578287015190505b61084285826107c4565b8655506108aa565b601f19841661085886610634565b60005b828110156108805784890151825560018201915060208501945060208101905061085b565b8683101561089d5784890151610899601f8916826107a6565b8355505b6001600288020188555050505b505050505050565b600081905092915050565b60006108c882610525565b6108d281856108b2565b93506108e2818560208601610541565b80840191505092915050565b60006108fa82846108bd565b91508190509291505056fea2646970667358221220faae786e52cca4060760290b1666e552a93e6e22cdebef07c8e90c367c2feefe64736f6c63430008120033"

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
nonce = nonce + 1
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
        "nonce": nonce,
    }
)

nonce = nonce + 1

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
        "nonce": nonce,
    }
)

nonce = nonce + 1

signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

tx_greeting_hash = w3.eth.send_raw_transaction(
    signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> add person >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


greeting_transaction = simple_storage.functions.addPerson('nagi', 2).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
nonce = nonce + 1

signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

tx_greeting_hash = w3.eth.send_raw_transaction(
    signed_greeting_txn.rawTransaction)
print("Updating person Value...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
