import time
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Order

logger = get_task_logger(__name__)


@shared_task
def process_order(order_id):
    time.sleep(10)
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.Status.PROCESSED
        order.save()
        logger.info(f"Заказ {order_id} был обработан.")
    except Order.DoesNotExist:
        logger.error(f"Заказ {order_id} не существует.")
    except Exception as e:
        logger.error(f"Ошибка обработки заказа {order_id}: {str(e)}")
