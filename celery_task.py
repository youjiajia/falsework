import logging
from celery import Celery

celery = Celery('celery')
celery.config_from_object('celery_settings')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
logger = logging.getLogger()


@celery.task
def test_task():
    logger.info(f"exit test task")
