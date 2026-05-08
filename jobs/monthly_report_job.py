from config.logger import get_logger
from jobs.scheduler import scheduler

logger = get_logger(__name__)


def run_monthly_report():
    logger.info("Running monthly report job")
    # Placeholder for monthly report aggregation logic
    pass


scheduler.add_job(run_monthly_report, 'cron', day=1, hour=0, minute=0, id='monthly_report_job')
