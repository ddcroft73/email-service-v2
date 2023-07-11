from schema import Email
from utils.smtp_email import smtp_email
from config.settings import settings
from utils.logger import logger

from celery import Task
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.timezone = 'US/Eastern'


# Experimenting with This setup... it may be more troublethan its worth.. lol
class EmailTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@celery.task(
    name="send_email_task",
    base=EmailTask,
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def send_email_task(self, email_dict: dict[str, str]):
    def on_retry(exc):
        pass

    def on_timeout(soft, timeout):
        pass

    try:
        email = Email(**email_dict)
        response = smtp_email.send_mail(email)
        return response

    except Exception as exc:
        raise self.retry(exc=exc, hook=on_retry)

    self.request.on_timeout = on_timeout

