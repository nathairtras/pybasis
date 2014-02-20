import arrow
from requests import Session

class basisAPI:
    """ Basis connection object

    :param str username: The username or email you use to log in to the Basis site
    :param str password: The password you use to log in to the Basis site
    """

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


    # Profile Initialization Methods
    # ===============

    def getMe(self):
        '''
        This will grab profile information like name, id, etc. Not necessary for methods below to work.
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
        This will grab the number of points. Not necessary for methods below to work.
        '''
        resp = self.session.get("https://app.mybasis.com/api/v1/points", headers=self.headers)
        self.points = resp.json()['points']


    # Sleep Methods
    # =============

    def sleepData(self,startdate, enddate=None):
        '''
        Get sleep data for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        If enddate is specified, gets sleep data for all dates in the range and returns them all in a list.
        '''
        startdate = arrow.get(startdate)

        if enddate:
            enddate = arrow.get(enddate)
            sleepList = []

            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleepData(date)
                for sleep in data:
                    sleepList.append(sleep)

            return sleepList

        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/activities?type=sleep&expand=activities.stages,activities.events", headers=self.headers)
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



    # Physiological Data
    # ==================

    def physData(self,date):
        '''
        Get physiological data for the date, over 60 second intervals
        '''
        date = arrow.get(date)
        resp = self.session.get("https://app.mybasis.com/api/v1/chart/me?summary=true&interval=60&units=ms&start_date=" + date.format('YYYY-MM-DD') + "&start_offset=0&end_offset=0&heartrate=true&steps=true&calories=true&gsr=true&skin_temp=true&air_temp=true&bodystates=true", headers=self.headers)
        return resp.json()

    # def crawlPhys(self, startdate, enddate):
    #     '''
    #     Gets physiological data for all dates in the range and returns them all in a list.
    #     '''
    #     startdate = arrow.get(startdate)
    #     enddate = arrow.get(enddate)
    #     dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
    #     phys = self.physData(dates.pop(0))
    #     for date in dates:
    #         data = self.physData(date)
    #         phys['timezone_history'] += data['timezone_history']
    #         phys['bodystates'] += data['bodystates']
    #         phys['endtime'] = data['endtime']
    #         for key in data['metrics'].keys():
    #             phys['metrics'][key]['values'] += data['metrics'][key]['values']
    #     for key in data['metrics'].keys():
    #         values = phys['metrics'][key]['values']
    #         phys['metrics'][key]['sum'] = sum(values)
    #         phys['metrics'][key]['avg'] = np.mean(values)
    #         phys['metrics'][key]['min'] = np.min(values)
    #         phys['metrics'][key]['max'] = np.max(values)
    #         phys['metrics'][key]['stdev'] = np.std(values)
    #
    #     return phys
