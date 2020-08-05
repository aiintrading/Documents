# sample code to connect to TrueData Http Feed
import requests
from time import sleep

pubip = "180.179.151.146"
userid = 'your_user_id'
password = 'your_password'

# Logout first
url_logout = 'http://%s/IDAUTH/Logout.aspx' % pubip

login_payload = "UserId=%s&Provider=TRUEDATA&Password=%s" % (userid, password)

headers = {
    'content-type': "application/x-www-form-urlencoded",
    # 'x-authz': key,
    'cache-control': "no-cache",
    }

response = requests.request("POST", url_logout, data=login_payload, headers=headers)

print(response.text)

# Login
url_login = "http://%s/IDAUTH/Login.aspx" % pubip

headers = {
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url_login, data=login_payload, headers=headers)

auth = response.text
key = auth.splitlines()[0]
# or Split the line on newlines and grab the first item from the result:
# key = auth.split('\n', 1)[0]
print(auth, '\n\n')
print('key =', key, '\n\n')


# SNAPM (To subscribe & get snapshot data of multiple symbols at the same time)
url_snapm = "http://%s/mxds/idmdata.aspx" % pubip

querystring = {"cmd": "SNAPM,%s" % userid}

symbols_payload = "1000007,1001330,1000010,1000022,1000025,1001153,1001594,1002885,1003787,1003045,1009479,1001336," \
                  "1003812,1000022,1011460,1000583,2048337,1013745,1015124,1002885,1003493,1000127,1000203,1003908," \
                  "1010940,1000308"

print('Subscribing to %s' % symbols_payload, '\n\n')
headers = {
    'x-authz': key,
    'cache-control': "no-cache",
    }

response = requests.request("POST", url_snapm, data=symbols_payload, headers=headers, params=querystring)

print(response.text)

# start a thread here for heartbeat
url_heartbeat = "http://%s/IDAUTH/Heartbeat.aspx" % pubip

headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-authz': key,
    'cache-control': "no-cache"
    }

response = requests.request("POST", url_heartbeat, data=login_payload, headers=headers)

print(response.text)

# start thread 2 for Mdata

seq_no = '0,0,0'

while True:
    
    url_mdata = "http://%s/mxds/idmdata.aspx" % pubip
    querystring = {"cmd": "d;MDATA,%s,%s" % (userid, seq_no)}
    headers = {
           'x-authz': key,
           'cache-control': "no-cache"
           }
    
    response = requests.request("POST", url_mdata, headers=headers, params=querystring)
    
    rtdata = response.text
    seq_no = rtdata.splitlines()[-1]
    print(rtdata, '------------')
    # print(seq_no)
    
    # wait for 0.8 secs
    # time1 = time()
    sleep(0.9)
    # time2 = time()
    # diff = time2 - time1
    # print('woken up in %s seconds' % diff)
