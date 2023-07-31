from app.schema import Email
from app.utils.smtp_email import smtp_email
from app.config.settings import settings
from app.utils.logger import logzz

from celery import Task
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.timezone = 'US/Eastern'


class EmailTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logzz.info(f"Email 'Task' [ Succeeded ] with a return value of: '{retval}' task.id: ({task_id})", timestamp=True)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logzz.error(f"Email 'Task' failed.", timestamp=True)

@celery.task(
    name="send_email_task",
    base=EmailTask,
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def send_email_task(self, email_dict: dict[str, str]):
    def on_retry(exc):
        logzz.error(
            f"\nResending email to: {email_dict.get('email_to', 'Unknown email')}\nDue to Exception: {str(exc)}", 
            timestamp=True
        )        
    try:
        email = Email(**email_dict)
        response = smtp_email.send_mail(email)
        return response

    except Exception as exc:
        on_retry(exc)
        raise self.retry(exc=exc)
    
