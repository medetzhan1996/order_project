from django.contrib import admin

from .tasks import process_order
from .models import Order, OrderAttachment


@admin.action(description="Отправить заказы на обработку")
def send_to_processing(modeladmin, request, queryset):
    for order in queryset:
        process_order.delay(order.id)


class OrderAttachmentInline(admin.TabularInline):
    model = OrderAttachment
    extra = 1  # Количество пустых форм для добавления новых прикреплений


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('order_number', 'user__phone')
    inlines = [OrderAttachmentInline]
    actions = [send_to_processing]
    ordering = ('-created_at',)


class OrderAttachmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'uploaded_at', 'file')
    list_filter = ('uploaded_at', 'order__order_number')
    search_fields = ('order__order_number',)
    ordering = ('-uploaded_at',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderAttachment, OrderAttachmentAdmin)
