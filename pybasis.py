"""
PyBasis :: An unofficial Basis python API client
"""

__author__ = 'jay weiler'
__version__ = "0.0.1"

import datetime
import arrow
from requests import Session

class API:

    def __init__(self, username,password):
        self.username = username
        self.password = password

        self.me = None
        self.points = None

        self.session = Session()
        self.login_payload = {"next": "https://app.mybasis.com", "username": self.username, "password": self.password, "submit": "Login"}

        self.session.post("https://app.mybasis.com/login", data=self.login_payload)
        self.access_token = self.session.cookies['access_token']
        self.refresh_token = self.session.cookies['refresh_token']
        self.headers = {"X-Basis-Authorization": "OAuth "+self.access_token}

    def getMe(self):
        resp = self.session.get("https://app.mybasis.com/api/v1/user/me.json", headers=self.headers)
        self.me = resp.json()

    def getPoints(self):
        resp = self.session.get("https://app.mybasis.com/api/v1/points", headers=self.headers)
        self.points = resp.json()['points']

    def sleepData(self,date):
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + date.format('YYYY-MM-DD') + "/activities?type=sleep&expand=activities.stages,activities.events", headers=self.headers)
        return resp.json()['content']['activities']

    def sleepSummary(self,date):
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + date.format('YYYY-MM-DD') + "/summary/activities/sleep", headers=self.headers)
        return resp.json()['content']

    def sleepActivities(self,date):
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + date.format('YYYY-MM-DD') + "/activities?type=sleep", headers=self.headers)
        return resp.json()['content']

    def crawlSleep(self, startdate, enddate):
        sleepList = []
        startdate = arrow.get(startdate)
        enddate = arrow.get(enddate)
        dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
        for date in dates:
            data = self.sleepData(date)
            for sleep in data:
                sleepList.append(sleep)

        return sleepList
