import arrow
from requests import Session

class BasisAPI:
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
    
    def profile_info(self):
        """
        This will grab profile information like name, id, etc. Not necessary for methods below to work.
        """
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

    def points(self):
        """
        This will grab the number of points. Not necessary for methods below to work.
        """
        resp = self.session.get("https://app.mybasis.com/api/v1/points", headers=self.headers)
        self.points = resp.json()['points']


    # Sleep Methods
    # =============

    def sleep_data(self,startdate, enddate=None):
        """
        Returns a list of sleep data for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        If enddate is specified, gets sleep data for all dates in the range and returns them all in the list.
        """
        startdate = arrow.get(startdate)
        results = []

        if enddate:
            enddate = arrow.get(enddate)

            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleep_data(date)
                results += data


        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/activities?type=sleep&expand=activities.stages,activities.events", headers=self.headers)
            results += resp.json()['content']['activities']

        return results

    def sleep_summary(self,startdate,enddate=None):
        """
        Returns a list with the sleep summary for a date as the element - can take a string in YYYY-MM-DD, datetime or
        arrow objects.
        If enddate is specified, gets sleep summaries for all dates in the range and returns them all as elements in the
        list.
        """
        startdate = arrow.get(startdate)
        results = []

        if enddate:
            enddate = arrow.get(enddate)
            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleep_summary(date)
                results += data

        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/summary/activities/sleep", headers=self.headers)
            results.append(resp.json()['content'])

        return  results

    def sleep_activities(self,startdate,enddate=None):
        """
        Returns a list of sleep activities for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        If enddate is specified, gets sleep activities for all dates in the range.
        """

        startdate = arrow.get(startdate)
        results = []

        if enddate:
            enddate = arrow.get(enddate)
            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleep_activities(date)
                results += data

        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/activities?type=sleep", headers=self.headers)
            results += resp.json()['content']['activities']

        return results



    # Physiological Data
    # ==================

    def phys_data(self, startdate, enddate=None):
        """
        Get physiological data for a date over 60 second intervals -- can take a string in 
        YYYY-MM-DD, datetime or arrow object. If enddate and metric arguments passed  are specified, gets physiological data for all
        dates in the range and returns metric in a list.
        """
        startdate = arrow.get(startdate)
        results = []

        if enddate:
            enddate = arrow.get(enddate)


            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.phys_data(date)
                results += data

        else:
            # this endpoint seems broken
            # resp = self.session.get("https://app.mybasis.com/api/v1/chart/me?summary=true&interval=60&units=ms&start_date=" + startdate.format('YYYY-MM-DD') + "&start_offset=0&end_offset=0&heartrate=true&steps=true&calories=true&gsr=true&skin_temp=true&air_temp=true&bodystates=true", headers=self.headers)
            resp = self.session.get("https://app.mybasis.com/api/v1/metricsday/me?day=" + startdate.format('YYYY-MM-DD') + "&heartrate=true&steps=true&calories=true&gsr=true&skin_temp=true&bodystates=true", headers=self.headers)
            results.append(resp.json())

        return results


    def phys_metrics(self, startdate, enddate=None, metrics=None):
        """
        Get one ore more physiological data metrics (steps, heartrate, calories, skin_temp, gsr) for a single day or
        range of days, and return an object containing those metrics, along with the start time, end time, and timezones
        during the collection.

        *gsr is skin perspiration
        """

        # This is the structure of the returned dictionary
        results = {'metrics': {}, 'starttime': None,'endtime': None, 'timezone_history' : []}

        # If metric exists and is not iterable (e.g. a string), make it so.
        if metrics and not hasattr(metrics, '__iter__'):
            metrics = [metrics]

        # If metric is not specified, get all of them
        if not metrics:
            metrics = ['skin_temp', 'heartrate', 'air_temp', 'calories', 'gsr', 'steps']

        # Create empty lists for each metric
        for metric in metrics:
            results['metrics'][metric] = []

        # Get all the data in range
        data = self.phys_data(startdate, enddate)

        if data:
            results['starttime'] = data[0]['starttime']
            results['endtime'] = data[0]['endtime']

            for element in data:
                results['starttime'] = min(results['starttime'], element['starttime'])
                results['endtime'] = max(results['endtime'], element['endtime'])
                results['timezone_history'] += element['timezone_history']

                for metric in metrics:
                    results['metrics'][metric] +=  element['metrics'][metric]['values']

        return results