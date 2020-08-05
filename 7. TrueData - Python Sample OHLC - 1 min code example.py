import requests


class TestTD():

    def __init__(self):

        self.pubip = "feed.truedata.in"
        self.userid = 'Enter_User_ID'
        self.password = 'Enter_Password'
        self.login_payload = 'UserId={}&Provider=TRUEDATA&Password={}'.format(self.userid, self.password)
        self.login_headers = {'cache-control': "no-cache", 'content-type': "application/x-www-form-urlencoded"}


    def login(self):
        # Login
        print('Attempting to Login')
        self.url_login = 'http://{}/IDAUTH/Login.aspx'.format(self.pubip)

        response = requests.request("POST", self.url_login, data=self.login_payload, headers=self.login_headers)

        auth = response.text
        self.key = auth.splitlines()[0]
        print('Key: ', self.key, '\n')

        # # or Split the line on newlines and grab the first item from the result:
        # # key = auth.split('\n', 1)[0]
        # print(auth, '\n\n')

        # PUB|180.179.151.146,180.179.151.146


    def logout(self):
        print('Attempting to Logout')
        # Logout first
        self.url_logout = 'http://{}/IDAUTH/Logout.aspx'.format(self.pubip)
        response = requests.request("POST", self.url_logout, data=self.login_payload, headers=self.login_headers)
        print(response.text)




    def ohlc(self):
        print('Attempting to get OHLC')

        ohlc_url = 'http://180.179.151.146/mxds/id1min.aspx?t=1000513&p=0'

        headers = {
            'cache-control': "no-cache",
            'x-authz': self.key,
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", ohlc_url, headers=headers)

        print('-' * 15)
        print(response.text)



app = TestTD()
app.logout()
app.login()
app.ohlc()