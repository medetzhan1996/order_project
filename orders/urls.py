from django.urls import path
from .views import OrderCreateView, OrderRetrieveView, OrderAttachmentCreateView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order-create'),
    path('<str:order_number>/', OrderRetrieveView.as_view(), name='order-retrieve'),
    path('<int:order_pk>/attachments/', OrderAttachmentCreateView.as_view(),
         name='order-attachment-create'),
]
