from web3 import Web3
from web3.middleware import geth_poa_middleware
import json, os


def mint_token(user_wallet):
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))
    contract_address = "0xB5Ef6aA58dba52fC26eF145C11aaC80b8BAfdEB9"
    private_key = os.getenv("PRIVATE_KEY") # to sign the transaction
    with open("missions/json/contract_abi.json", "r") as f:
        contract_abi = json.load(f)

    # Inject PoA middleware for networks using Proof of Authority consensus
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    nonce = w3.eth.get_transaction_count(os.getenv("WEB3_NONCE"))
    # Verify if the connection is successful
    # if w3.is_connected():
    #     print("-" * 50)
    #     print("Connection Successful")
    #     print("-" * 50)
    # else:
    #     print("Connection Failed")
        
    # Load the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # ----------------------------------- CALL FUNCTIONS AND TRANSACTIONS -----------------------------------

    amount_to_mint = 1 * 10**18 # Amount of tokens will be minted

    transaction = contract.functions.mintTo(user_wallet, amount_to_mint).build_transaction({
        'gas': 100000, 
        'nonce': nonce,
        'chainId': 80001 # this is the chain id of Mumbai. When switching to mainnet, use 137
    })

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print("Transaction receipt is: ", receipt)

    