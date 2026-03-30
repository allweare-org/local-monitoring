import socket
import ipaddress
import subprocess

# -----------------------------
# CONFIG
# -----------------------------
SUBNET = "192.168.1.0/24"   # Change only if needed
PORT = 8899
TIMEOUT = 0.5

# -----------------------------
# CHECK PORT
# -----------------------------
def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            result = sock.connect_ex((str(ip), port))
            return result == 0
    except:
        return False

# -----------------------------
# GET MAC (optional)
# -----------------------------
def get_mac(ip):
    try:
        output = subprocess.check_output(["arp", "-n", str(ip)]).decode()
        return output.strip()
    except:
        return ""

# -----------------------------
# MAIN SCAN
# -----------------------------
def find_logger():
    print(f"Scanning {SUBNET} for devices with port {PORT} open...\n")

    network = ipaddress.ip_network(SUBNET, strict=False)
    candidates = []

    for ip in network.hosts():
        ip_str = str(ip)
        if is_port_open(ip_str, PORT):
            mac_info = get_mac(ip_str)
            print(f"✅ Found device with port {PORT} open: {ip_str}")
            print(f"   MAC info: {mac_info}\n")
            candidates.append(ip_str)

    if not candidates:
        print("❌ No devices found with port 8899 open.")
    else:
        print("🎯 Likely logger IP(s):")
        for c in candidates:
            print(f"   → {c}")

    return candidates


if __name__ == "__main__":
    find_logger()