import logging
from typing import Dict, Union
from celery import shared_task
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    logger.info(f"Send message: '{message_form}'")
    send_mail(
        message_form["message"],  # message
        ["techsupport@braniac.com"],  # send to
        from_email="email_address",  # send from
        fail_silently=False,
    )
    return None
