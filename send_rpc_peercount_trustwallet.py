import requests
import time

# 函数：向URL发送RPC请求，获取net_peerCount
def get_peer_count(url):
    try:
        response = requests.post(url, json={"jsonrpc": "2.0", "method": "net_peerCount", "params": [], "id": 1})
        if response.status_code == 200:
            return response.json().get('result', 'Unknown')
        else:
            return {"error": f"HTTP Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 主函数：循环发送RPC请求并输出结果去重
def main(url, interval=0.1):
    seen_results = set()  # 存储已经见过的结果，用于去重
    while True:
        result = get_peer_count(url)
        if isinstance(result, dict) and 'error' in result:
            print(result['error'])
            continue
        if result not in seen_results:
            print(result)
            seen_results.add(result)
        time.sleep(interval)

if __name__ == "__main__":
    url = "https://ethereum.twnodes.com"  # 替换成你要发送RPC请求的URL
    main(url)
