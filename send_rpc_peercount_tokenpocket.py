import requests

# 函数：从txt文件中读取IP地址列表
def read_ips_from_file(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    ips = [ip.strip() for ip in ips]  # 移除每行末尾的换行符
    return ips

# 函数：向IP地址发送RPC请求，获取net_peerCount
def get_peer_count(ip, port):
    try:
        url = f"http://{ip}:{port}"
        response = requests.post(url, json={"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":1})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 函数：将IP地址及其回复消息写入txt文件
def write_response_to_file(ip_responses_dict, output_file, success_output_file):
    with open(output_file, 'w') as file, open(success_output_file, 'w') as success_file:
        for ip, response in ip_responses_dict.items():
            file.write(f"IP: {ip}\n")
            file.write(f"Response: {response}\n\n")
            if response.get('result') == "0x1e":
                success_file.write(f"{ip}\n")

# 主函数
def main(input_file, output_file, success_output_file, port="8545"):
    ips = read_ips_from_file(input_file)
    ip_responses_dict = {}
    for ip in ips:
        response = get_peer_count(ip, port)
        ip_responses_dict[ip] = response
    write_response_to_file(ip_responses_dict, output_file, success_output_file)

if __name__ == "__main__":
    input_file = "now_openrpc-ip_305.txt"  # 输入txt文件路径
    output_file = "ip_peercount_20240531.txt"  # 输出txt文件路径
    success_output_file = "filterips_tokenpocket.txt"  # 输出成功IP地址的txt文件路径
    port = "8545"  # RPC端口号
    main(input_file, output_file, success_output_file, port)
