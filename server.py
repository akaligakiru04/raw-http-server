import socket
import json

HOST = '127.0.0.1'
PORT = 50007

LINES = '''2026-10-23T05:11:28.098457+02:00 Farah sshd[12739]: Failed password for invalid user 0101 from 203.0.113.15 port 34990 ssh2
2026-10-23T11:02:20.865470+02:00 Farah sudo: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
2026-10-23T05:11:28.098457+02:00 Farah sshd[12740]: Connection closed by 203.0.113.5 port 22 [preauth]'''

def response_bytes(request_bytes):
    body = json.dumps(LINES).encode("utf-8")
    headers = "200 OK\n" + "Content-Type:application/json\n" + "Content-Length:" + len(LINES.encode("utf-8")) + "\n\n"
    headers = headers.encode("utf-8")
    return (headers,body)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(1) #i guess this means s is the server and its now listening, 1 maybe means True? so listen at all times?
    while True:
        conn, addr = s.accept() #get some sort of address? ip address?
        with conn:
            print('connected by', addr)
            full_data = b''
            print(full_data[-8:])
            while b'\r\n\r\n' not in full_data:
                print("last five: " ,full_data[-5:])
                data = conn.recv(1024) #receive 1024 bytes or something?
                full_data += data
                print(repr(data))
                if not data: break
                conn.sendall(response_bytes(data))
            print("recv loop over")
        print("connection closed")


