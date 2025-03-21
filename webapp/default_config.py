# The default_config module automatically gets imported by Appconfig, if it
# exists. See https://pypi.python.org/pypi/flask-appconfig for details.

# Note: Don't *ever* do this in a real app. A secret key should not have a
#       default, rather the app should fail if it is missing. For the sample
#       application, one is provided for convenience.
SECRET_KEY = 'devkey'
BOOTSTRAP_SERVE_LOCAL=True
INFRAMON_CONFIG_FILE = "conf/inframon.json"
VERBOSE= True
DEBUG = True
# cache config
CACHE_TYPE="SimpleCache"
CACHE_DEFAULT_TIMEOUT=300 # seconds