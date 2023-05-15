import re
import subprocess
import time

INTERFACE = "wg0"

def process_peer(public_key, endpoint):
    result = subprocess.run(["wg", "show", INTERFACE, "latest-handshakes"], capture_output=True, text=True)
    escaped_public_key = re.escape(public_key)
    match = re.search(f"{escaped_public_key}\t([0-9]+)", result.stdout)
    #print(f"Result mmm: {len(result.stdout)}")
    if match:
        #print(f"Key: {key}, Value: {value}")
        epoch_seconds = int(match.group(1))
        #print(f"Seconds: {epoch_seconds}")
        numero = (time.time() - epoch_seconds)
        formatado = f"{numero:.3f}".replace('.', ',')
        if (numero) > 135:
            #subprocess.run(["wg", "set", INTERFACE, "peer", public_key, "endpoint", endpoint])
            #print("sim")
            print(f"Peer: {public_key} -> Down for: {formatado} seconds")
            print("restarting...")
            result = subprocess.run(["systemctl", "restart", "wg-quick@wg0.service"],capture_output=True, text=True)
        else:
            print(f"Peer: {public_key} -> UP _ Last Handshake: {formatado} seconds")
def reset_peer_section():
    global peer_section, public_key, endpoint
    peer_section = False
    public_key = ""
    endpoint = ""

reset_peer_section()
with open("/etc/wireguard/wg0.conf", "r") as f:
    for line in f:
        line = line.split("#", 1)[0].strip() # Remove comentários e espaços em branco
        if not line:
            continue
        if line.startswith("[Peer]"):
            #print("peer")
            peer_section = True
        elif peer_section:
            match = re.match(r"\s*(\S+)\s*=\s*(.*)\s*", line)
            if match:
                key = match.group(1)
                value = match.group(2)
                if key == "PublicKey":
                    if not re.match(r"^[A-Za-z0-9/+.-]{43}=$", value):
                        continue
                    public_key = value
                    #print(f"Key: {key}, Value: {value}")
                elif key == "Endpoint":
                    endpoint = value
                    #print(f"Key: {key}, Value: {value}")'
            process_peer(public_key, endpoint)
            reset_peer_section()
