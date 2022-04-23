from requests import get
local_host = get('https://api.ipify.org').content.decode('utf8')
print('Local host =', local_host)

import ipaddress
mask = ipaddress.IPv4Network(local_host)
print('Mask =', mask.netmask)
