import socket
import struct
import time
import random

HOST = "0.0.0.0"
PORT = 8899

# --- Fake inverter data ---
def build_fake_modbus_response():
    # Fake values (you can expand this later)
    voltage = int(220 + random.random() * 10)
    current = int(5 + random.random() * 2)
    power = int(voltage * current)

    # Pack into bytes (very simplified Modbus-style payload)
    payload = struct.pack(">HHH", voltage, current, power)
    return payload

def handle_client(conn):
    print("Client connected")

    try:
        while True:
            # Simulate periodic inverter response
            data = build_fake_modbus_response()

            # Send length + payload (very simplified framing)
            conn.sendall(data)

            time.sleep(2)

    except Exception as e:
        print("Client disconnected:", e)
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Mock Solarman server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print("Connection from", addr)
        handle_client(conn)

if __name__ == "__main__":
    main()