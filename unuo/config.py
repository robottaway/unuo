"""Configuration specific code.

DefaultConfig is the app wide default configuration for unuo. If you want to
override that config use UNUO_CONF environment variable to point to a cfg
file. See http://flask.pocoo.org/docs/config/#development-production for more
info.
"""


class DefaultConfig(object):
    DEBUG = True
    env = 'dev'
    # default filestore locations
    builds_folder = '/var/local/unuo'
    logs_folder = '/var/log/unuo'

config = DefaultConfig()
