from .crontabs import Crontabs

schedule = {
    # 'run-every-minute': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_minute,
    #     'args': (100, )
    # },
    # 'run-every-2-minutes': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_2_minutes,
    #     'args': (200,)
    # },
    # 'run-every-hour': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_hour,
    #     'args': (6000,)
    # },
    'run-every-hour-2': {
        'task': 'task_delete_expired_sessions',
        'schedule': Crontabs.every_day,
        'args': tuple()
    },
    'run-every-hour-3': {
        'task': 'task_delete_expired_tokens',
        'schedule': Crontabs.every_day,
        'args': tuple()
    },
    # 'run-every-10-minutes': {
    #     'task': 'task_beat_test_every_minute',
    #     'schedule': Crontabs.every_10_minutes,
    #     'args': (1000,)
    # },
    # 'run-every-day': {
    #     'task': None,
    #     'schedule': Crontabs.every_day,
    #     'args': (10, 20)
    # },
}