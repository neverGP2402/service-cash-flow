from config.logger import get_logger
from jobs.scheduler import scheduler

logger = get_logger(__name__)


def run_exchange_rate_update():
    logger.info("Running exchange rate update job")
    # Placeholder for exchange rate update logic
    pass


scheduler.add_job(run_exchange_rate_update, 'interval', hours=6, id='exchange_rate_job')
