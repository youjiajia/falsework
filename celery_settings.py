import helper
from celery.schedules import crontab
import logging


_config = helper.get_config()

broker_url = _config.get('mq', {}).get('broker_url', 'redis://127.0.0.1:6379/5')
logging.info(broker_url)


# CELERY_TIMEZONE = 'UTC'
# CELERY_ENABLE_UTC = True
#

# CELERY_QUEUES = (
#     Queue('xx_task', Exchange('xxx_xxx')),
# )
#
# CELERY_ROUTES = {
#     'celery_tasks.save_watch_event': {'queue': 'user_watch'},
# }
# 导入任务所在文件
imports = [
    "celery_task"
]


# 需要执行任务的配置
beat_schedule = {
    "test_task": {
        "task": "celery_task.test_task",
        "schedule": crontab(minute="*/10"),   # every minute 每十分钟执行
        "args": ()  # # 任务函数参数
    },
}
