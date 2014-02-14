"""
PyBasis :: An unofficial Basis python API client
"""

__author__ = 'jay weiler'
__version__ = "0.0.1"

from requests import Session

class API:

    def __init__(self,username,password):
        self.username = username
        self.password = password

        self.me = None
        self.points = None

        self.session = Session()
        self.login_payload = {"next":"https://app.mybasis.com","username": self.username,"password": self.password,"submit": "Login"}

        self.session.post("https://app.mybasis.com/login",data = self.login_payload)
        self.access_token = self.session.cookies['access_token']
        self.refresh_token = self.session.cookies['refresh_token']
        self.headers = {"X-Basis-Authorization": "OAuth "+self.access_token}

    def getMe(self):
        resp = self.session.get("https://app.mybasis.com/api/v1/user/me.json",headers=self.headers)
        self.me = resp.json()

    def getPoints(self):
        resp = self.session.get("https://app.mybasis.com/api/v1/points", headers=self.headers)
        self.points = resp.json()['points']