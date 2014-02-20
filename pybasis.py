"""
PyBasis :: An unofficial Basis python API client
"""

__author__ = 'jay weiler'
__version__ = "0.0.1"

import arrow
from requests import Session

class basis:
    '''
    Basis connection object
    '''

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.me = None
        self.points = None

        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.email = None
        self.joined = None
        self.level = None
        self.id = None
        self.device = None
        self.last_synced = None
        self.anatomy = None

        self.session = Session()
        self.login_payload = {"next": "https://app.mybasis.com", "username": self.username, "password": self.password, "submit": "Login"}

        self.session.post("https://app.mybasis.com/login", data=self.login_payload)
        self.access_token = self.session.cookies['access_token']
        self.refresh_token = self.session.cookies['refresh_token']
        self.headers = {"X-Basis-Authorization": "OAuth "+self.access_token}


    # Profile Intialization Methods
    # ===============

    def getMe(self):
        '''
        This will grab profile information like name, id, etc. Not necessary for calls below to work.
        '''
        resp = self.session.get("https://app.mybasis.com/api/v1/user/me.json", headers=self.headers)
        self.me = resp.json()
        self.first_name = self.me['profile']['first_name']
        self.last_name = self.me['profile']['last_name']
        self.full_name = self.me['profile']['full_name']
        self.email = self.me['email']
        self.joined = arrow.get(self.me['profile']['joined'])
        self.level = self.me['level']
        self.id = self.me['id']
        self.device = self.me['device']
        self.last_synced = arrow.get(self.me['last_synced'])
        self.anatomy = self.me['anatomy']

    def getPoints(self):
        '''
        This will grab the number of points. Not neccessary for method to work.
        '''
        resp = self.session.get("https://app.mybasis.com/api/v1/points", headers=self.headers)
        self.points = resp.json()['points']


    # Sleep Methods
    # =============

    def sleepData(self,date):
        '''
        Get sleep data for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        '''
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + date.format('YYYY-MM-DD') + "/activities?type=sleep&expand=activities.stages,activities.events", headers=self.headers)
        return resp.json()['content']['activities']

    def sleepSummary(self,date):
        '''
        Get sleep summary for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        '''
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + date.format('YYYY-MM-DD') + "/summary/activities/sleep", headers=self.headers)
        return resp.json()['content']

    def sleepActivities(self,date):
        '''
        Get sleep activities for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        '''
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + date.format('YYYY-MM-DD') + "/activities?type=sleep", headers=self.headers)
        return resp.json()['content']

    def crawlSleep(self, startdate, enddate):
        '''
        Gets sleep data for all dates in the range and returns them all in a list.
        '''
        sleepList = []
        startdate = arrow.get(startdate)
        enddate = arrow.get(enddate)
        dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
        for date in dates:
            data = self.sleepData(date)
            for sleep in data:
                sleepList.append(sleep)

        return sleepList
