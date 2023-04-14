import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

load_dotenv()


def Deploy_Contract(Contract_path, install_solc_v="0.6.0"):
    with open(Contract_path, "r") as file:
        simple_storage_file = file.read()

    # We add these two lines that we forgot from the video!
    print("Installing... solc")
    install_solc(install_solc_v)

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

    # get abi
    abi = json.loads(
        compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
    )["output"]["abi"]
    os.remove("compiled_code.json")

    return abi, bytecode
