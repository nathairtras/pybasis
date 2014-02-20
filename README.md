pybasis
=======

Unofficial python library for accessing the Basis API at https://app.mybasis.com

**Only supports sleep data at the moment**

Heavily inspired by [hof](https://github.com/hof)'s [basis-java-api](https://github.com/hof/basis-java-api)

Requirements: 

- [requests](http://requests.readthedocs.org/en/latest/)
- [arrow](http://crsmithdev.com/arrow/)

Usage:

```python

>>> import pybasis
>>> api = pybasis.basisAPI("username","password")

>>> api.sleepData('2014-02-12')
[{u'actual_seconds': 7320,
  u'calories': 145.5,
  u'end_time': {u'iso': u'2014-02-13T10:47:00Z',
                u'time_zone': {u'name': u'America/Los_Angeles',
                               u'offset': -480},
                u'timestamp': 1392288420},
  u'events': [{u'time': {u'iso': u'2014-02-13T09:19:00Z',
  ...
  },
  { ... },
  ...]
  
>>> api.sleepSummary('2014-02-12')
{u'heart_rate': {u'avg': 58.76611901575547}, 
u'interruption_minutes': 0, u'minutes': 215, u'calories': 461.09999999999997, 
u'rem_minutes': 74, u'light_minutes': 255, u'deep_minutes': 60, 
u'date': u'2014-02-12', u'interruptions': 0.0, u'quality': 31.0, 
u'toss_and_turn': 6}

>>> api.sleepActivities('2014-02-12')
{u'activities': [{u'type': u'sleep', u'link': u'/v2/users/51635464rts10031da/activities/52fe5050ee8f134da5914f65'}, 
{u'type': u'sleep', u'link': u'/v2/users/51635464rts10031da/activities/52fe5050ee8f134da5914f67'}]}

>>> api.crawlSleep('2014-02-05','2014-02-12')
[{u'actual_seconds': 7320,
  u'calories': 145.5,
  u'end_time': {u'iso': u'2014-02-13T10:47:00Z',
                u'time_zone': {u'name': u'America/Los_Angeles',
                               u'offset': -480},
                u'timestamp': 1392288420},
  u'events': [{u'time': {u'iso': u'2014-02-13T09:19:00Z',
  ...
  },
  { ... },
  { ... },
  ...]


```