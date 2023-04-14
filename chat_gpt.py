# import web3 and json modules
import json
from web3 import Web3

# connect to the Ethereum network using Infura node endpoint
w3 = Web3(Web3.HTTPProvider(
    'https://polygon-mumbai.g.alchemy.com/v2/K59YdNGK95akCLJrA1m9nYPZ7JYNa8Me'))

# set the account address and private key
my_address = '0x042bDdB896fa2B4F5993e3926b7dD53B27f9321E'
private_key = '0x6021d22205954e378994c07b70dae0afd8e67b5eb61c8f799ebfd24f5f010708'

# set the contract address and ABI
contract_address = '0x52B4100E9474f731C67f43E5C0A24Db756De6c4A'
contract_abi = json.loads('[{"inputs":[],"name":"retrieve","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint256","name":"_favoriteNumber","type":"uint256"}],"name":"addPerson","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_favoriteNumber","type":"uint256"}],"name":"store","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# create an instance of the contract
simple_storage = w3.eth.contract(address=contract_address, abi=contract_abi)

print("contract get..")
# get the nonce for the transaction
nonce = w3.eth.getTransactionCount(my_address)

# build the transaction to set the storage value to 2
greeting_transaction = simple_storage.functions.store(2).buildTransaction(
    {
        "chainId": w3.eth.chainId,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,  # the initial nonce should "orginal nonce value" after that you should be increase nonce
    }
)
print("transaction sucess..")

# sign the transaction with the private key
signed_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key)

# send the signed transaction to the network
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# print the transaction hash and the new storage value
print(f'Transaction hash: {tx_receipt.transactionHash.hex()}')
print(f'New storage value: {simple_storage.functions.retrieve().call()}')
