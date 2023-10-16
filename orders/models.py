from random import randint

from django.db import models, IntegrityError
from django.conf import settings


class Order(models.Model):
    class Status(models.TextChoices):
        PROCESSING = 'processing', 'В обработке'
        PROCESSED = 'processed', 'Обработанный'

    class SiteType(models.TextChoices):
        BLOG = 'blog', 'Блог'
        ECOMMERCE = 'ecommerce', 'Интернет-магазин'
        PERSONAL = 'personal', 'Личный сайт'
        CORPORATE = 'corporate', 'Корпоративный сайт'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=6, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROCESSING)
    site_type = models.CharField(max_length=20, choices=SiteType.choices)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_order_number(cls):
        """Генерирует уникальный случайный шестизначный номер."""
        number = '{:06}'.format(randint(1, 999999))
        while cls.objects.filter(order_number=number).exists():
            number = '{:06}'.format(randint(1, 999999))
        return number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        try:
            super(Order, self).save(*args, **kwargs)
        except IntegrityError:
            # Генерируем новый и пытаемся снова
            self.order_number = self._generate_order_number()
            super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.order_number)


class OrderAttachment(models.Model):
    order = models.ForeignKey(Order, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='order_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

