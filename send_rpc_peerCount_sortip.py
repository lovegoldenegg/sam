import json
import requests
from collections import Counter


def read_ips_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def send_net_peerCount(ip):
    url = f'http://{ip}:8545'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "net_peerCount",
        "params": [],
        "id": 1
    })

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        # 提取并转换peer count
        if 'result' in result and isinstance(result['result'], str):
            peer_count_hex = result['result']
            peer_count = int(peer_count_hex, 16)
            return peer_count
        else:
            print(f"Invalid response from {ip}: {result}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {ip}: {e}")
        return None


def main(input_file, output_file):
    ips = read_ips_from_file(input_file)
    ip_peer_counts = []

    for ip in ips:
        peer_count = send_net_peerCount(ip)
        if peer_count is not None:
            ip_peer_counts.append((ip, peer_count))
            print(f"{ip} has {peer_count} peers")

    # 按peer count从大到小排序
    sorted_ip_peer_counts = sorted(ip_peer_counts, key=lambda x: x[1], reverse=True)

    # 统计每个 peer count 的出现次数
    peer_count_counter = Counter(count for ip, count in sorted_ip_peer_counts)

    with open(output_file, 'w') as file:
        for ip, count in sorted_ip_peer_counts:
            file.write(f"{ip}: {count}\n")

        file.write("\nPeer count frequencies:\n")
        for count, freq in peer_count_counter.items():
            file.write(f"{count} peers: {freq} times\n")

    print("IP addresses sorted by peer count:")
    for ip, count in sorted_ip_peer_counts:
        print(f"{ip}: {count}")

    print("\nPeer count frequencies:")
    for count, freq in peer_count_counter.items():
        print(f"{count} peers: {freq} times")


if __name__ == "__main__":
    input_file = 'now_openrpc-ip_308.txt'
    output_file = 'sorted_ips_20240531.txt'
    main(input_file, output_file)
