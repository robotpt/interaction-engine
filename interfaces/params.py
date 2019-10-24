from pickled_database import PickledDatabase
import datetime


params_db = PickledDatabase()

params_db.create_key_if_not_exists(
    'param1', 1
)
