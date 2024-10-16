import time

import requests
import json
from web3 import Web3
from eth_account import Account
from eth_utils import to_checksum_address

def send_raw_transaction(url, raw_transaction):
    # 构造RPC消息
    rpc_message = {
        "jsonrpc": "2.0",
        "method": "eth_sendRawTransaction",
        "params": [raw_transaction],
        "id": 1
    }
    start_time = time.time()  # 记录开始时间
    # 发送POST请求
    response = requests.post(url, json=rpc_message)
    end_time = time.time()  # 记录结束时间

    # 计算代码运行时间
    execution_time = end_time - start_time

    print("hanshu运行时间：", execution_time, "秒")
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容
        response_json = response.json()
        if "result" in response_json:
            return response_json["result"]
        elif "error" in response_json:
            raise Exception("Error: " + response_json["error"]["message"])
        else:
            raise Exception("Unknown response format")
    else:
        raise Exception("HTTP request failed with status code: " + str(response.status_code))

if __name__ == "__main__":
    # url = "https://rpc.sepolia.org"  # 替换为你的URL
    url="https://eth-mainnet.token.im"
    sender_address = "0x75617210Da0b5C9337d45d69fC8969D07E14F938"  # 替换为发送方地址
    sender_private_key = "99a8e3da1c523229e07d3724081f998ed7f9d0df2f1da76a1ec7f47ff3df147c"  # 替换为发送方私钥
    receiver_address = "0x75617210Da0b5C9337d45d69fC8969D07E14F938"  # 替换为接收方地址
    value_eth = 0  # 以太币数量

    # 连接以太坊节点
    w3 = Web3(Web3.HTTPProvider(url))

    # 构建交易的字典数据
    nonce = w3.eth.get_transaction_count(sender_address)
    value = Web3.to_wei(value_eth, "ether")
    gas_price = w3.eth.gas_price
    chain_id = w3.eth.chain_id
    print("chain id:",str(chain_id))
    print("Gas price: " + str(gas_price))
    transaction = {
        'to': to_checksum_address(receiver_address),
        'value': value,
        'gas': 21000,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': chain_id,
    }

    # 使用发送方私钥对交易进行签名
    signed_txn = w3.eth.account.sign_transaction(transaction, sender_private_key)

    # 获取原始交易数据
    raw_transaction = signed_txn.rawTransaction.hex()

    try:
        start_time = time.time()  # 记录开始时间
        tx_hash = send_raw_transaction(url, raw_transaction)
        end_time = time.time()  # 记录结束时间

        # 计算代码运行时间
        execution_time = end_time - start_time

        print("代码运行时间：", execution_time, "秒")
        print("交易哈希:", tx_hash)
    except Exception as e:
        print("发送交易失败:", str(e))
