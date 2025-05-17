
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_card_system.settings')

app = Celery('credit_card_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(
    broker_url=os.getenv('MONGODB_URL'),
    result_backend=os.getenv('MONGODB_URL')
)