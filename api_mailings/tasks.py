import os
import requests
import pytz
import datetime
from celery.utils.log import get_task_logger

from .models import Message, Mailings, Client
from test_task_fabrikaReshenji.celery import app

logger = get_task_logger(__name__)

URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')

@app.task(bind=True, retry_backoff=True)
def send_message(self, data, mailing_id, client_id, url=URL, token=TOKEN):
    mailing = Mailings.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.time_zone)
    now = datetime.datetime.now(timezone)

    if mailing.start_time <= now.time() <= mailing.end_time:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            logger.error(f"Message if: {data['id']} is error")
            raise self.retry(exc=exc)
        else:
            logger.info(f"Message id: {data['id']}, Sending status: 'Sent'")
            Message.objects.filter(pk=data['id']).update(status_of_shipping='Sent')
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                     int(mailing.start_time.strftime('%H:%M:%S')[:2]))
        logger.info(f"Message id: {data['id']}, "
                    f"The current time is not for sending the message,"
                    f"restarting task after {60*60*time} seconds")
        return self.retry(countdown=60*60*time)


