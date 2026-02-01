import requests
from bs4 import BeautifulSoup
from z3 import Int, Solver, sat
from Crypto.Util.number import isPrime

host = 'http://localhost:8888'
username = 'Kirito'

DAEMONS = [
    ("systemd", "A system and service manager."),
    ("crond", "A daemon to execute scheduled commands."),
    ("sshd", "The OpenSSH daemon."),
    ("httpd", "The Apache HTTP server."),
    ("mysqld", "The MySQL database server."),
    ("nginx", "An HTTP and reverse proxy server."),
    ("dbus-daemon", "A message bus system."),
    ("cupsd", "The CUPS print server."),
    ("udevd", "A device manager for the Linux kernel."),
    ("smbd", "The Samba daemon for file and print services."),
    ("rsyslogd", "A logging daemon."),
    ("NetworkManager", "A daemon for managing network connections."),
    ("polkitd", "Authorization manager for applications."),
    ("named", "The BIND DNS daemon."),
    ("postfix", "A mail transfer agent."),
    ("iptables", "A user-space firewall utility."),
    ("auditd", "The Linux Audit System daemon."),
    ("wpa_supplicant", "A Wi-Fi Protected Access client."),
    ("dhcpd", "A DHCP server daemon."),
    ("nfsd", "The NFS server kernel thread daemon."),
    ("rpcbind", "A server that converts universal addresses to program numbers."),
    ("avahi-daemon", "A zero-configuration networking daemon."),
    ("snapd", "A daemon for managing snap packages."),
    ("containerd", "A container runtime daemon."),
    ("dockerd", "The Docker daemon."),
    ("lighttpd", "A lightweight web server."),
    ("vlc", "A multimedia player daemon."),
    ("chronyd", "A daemon for time synchronization."),
    ("pulseaudio", "A sound system daemon."),
    ("modemmanager", "A service for managing modems."),
    ("upowerd", "A service for power management."),
    ("squirreld", "🐿️🪑🎹.")
]

for i in range(9):
  r = requests.post(f'{host}/register', data={
    'username': username, 'password': '1234'})

s = requests.session()
s.post(f'{host}/login', data={
  'username': username, 'password': '1234'})

hints = []
for j in range(7):
  payload = ['0'] * 9
  payload[j] = '1'
  res = s.post(f'{host}/draw', json={'numbers': payload}).json()
  print(res)
  for i, daemon in enumerate(DAEMONS):
    if daemon[0] == res['name']:
      idx0 = i
    if daemon[1] == res['description']:
      idx1 = i
  hints.append((idx0, idx1, res['id']))

payload = ['0'] * 9
payload[7], payload[8] = '1', hex(1 << 128)
res = s.post(f'{host}/draw', json={'numbers': payload}).json()
hints += [(None, None, res['id'] % (1 << 128)), (None, None, res['id'] >> 128)]

print(hints)

def egcd(a: int, b: int):
  a, coe_a =  (a, (1, 0)) if (a > 0) else (-a, (-1, 0))
  b, coe_b =  (b, (0, 1)) if (b > 0) else (-b, (0, -1))
  q, r = a // b, a % b
  while r:
    a, b, coe_a, coe_b = b, r, coe_b, (coe_a[0] - q * coe_b[0], coe_a[1] - q * coe_b[1])
    q, r = a // b, a % b
  return coe_b

res = s.get(f'{host}/game')
soup = BeautifulSoup(res.text, 'html.parser')
pub_mask = eval(soup.select('pre')[0].text)
pub_vector = eval(soup.select('pre')[1].text)

vector = []
for i in range(9):
  a, b = pub_mask[0], pub_mask[1]
  c = pub_vector[i] - hints[i][2] * pub_mask[2]
  x, y = Int('x'), Int('y')
  sol = Solver()
  sol.add(a * x + b * y == c)
  sol.add(x > 0)
  sol.add(y > 0)
  if sol.check() == sat:
    m = sol.model()
    x, y = m[x].as_long(), m[y].as_long()

  x_list, y_list = [x], [y]
  newx, newy = x, y
  while True:
    newx, newy = newx - b, newy + a
    if newx < 0:
      break
    x_list.append(newx)
    y_list.append(newy)
  newx, newy = x, y
  while True:
    newx, newy = newx + b, newy - a
    if newy < 0:
      break
    x_list.append(newx)
    y_list.append(newy)
  for x, y in zip(x_list, y_list):
    if (not isPrime(x)) or (not isPrime(y)):
      continue
    if hints[i][0] is not None and x % 32 != hints[i][0]:
      continue
    if hints[i][1] is not None and y % 32 != hints[i][1]:
      continue
    vector.append(x)

res = s.post(f'{host}/draw', json={'numbers': [hex(num) for num in vector]}).json()
print(res)
