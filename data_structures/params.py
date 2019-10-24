from pickled_database import PickledDatabase

params_file = 'params.pkl'
params_db = PickledDatabase(params_file)

params_db.create_key_if_not_exists(
    'param1', 1
)
