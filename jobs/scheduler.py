from apscheduler.schedulers.background import BackgroundScheduler
from config.logger import get_logger

logger = get_logger(__name__)
scheduler = BackgroundScheduler()


def start_scheduler():
    logger.info("Starting background scheduler")
    scheduler.start()


def shutdown_scheduler():
    logger.info("Shutting down background scheduler")
    scheduler.shutdown()
