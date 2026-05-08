from config.logger import get_logger
from jobs.scheduler import scheduler

logger = get_logger(__name__)


def run_debt_reminder():
    logger.info("Running debt reminder job")
    # Placeholder for debt reminder logic
    pass


scheduler.add_job(run_debt_reminder, 'cron', hour=8, minute=0, id='debt_reminder_job')
