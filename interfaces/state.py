from pickled_database import PickledDatabase
import datetime


state_db = PickledDatabase()

state_db.create_key_if_not_exists(
    'user_input'
)
state_db.create_key_if_not_exists(
    'user_name',
    tests=lambda x: type(x) is str
)
state_db.create_key_if_not_exists(
    'first_meeting',
    tests=lambda x: type(x) is datetime.datetime
)
