from django.contrib import admin
from django.http import HttpRequest

from .models import Category, Product

#простой способ
#admin.site.register(Category)

#крутой способ
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.action(description="Raise price", permissions=["change"])
def raise_price(self, request, queryset):
    for obj in queryset:
        obj.price += obj.price * 0.05
        obj.save(update_fields=["price"])
    self.message_user(request, "Successfully raised price!")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name", "art")
    list_display = ("name", "art", "price", "count")
    list_filter = ("category",)
    list_editable = ("price", "count")
    actions = ("raise_price",)

class GroupAdminSite(admin.AdminSite):
    def __init__(self, name, title, group_name):
        super().__init__(name=name)
        self.site_header = title
        self.site_title = title
        self.group_name = group_name

    def has_permission(self, request):
        return super().has_permission(request)

MANAGER_GROUP = "Managers"
WAREHOUSE_GROUP = "Warehouses"

manager_site = GroupAdminSite(
    "manager_admin",
    "Панель менеджера",
    MANAGER_GROUP
)

warehouse_site = GroupAdminSite(
    "warehouse_admin",
    "Панель сотрудника склада",
    WAREHOUSE_GROUP
)

@admin.register(Product, site=manager_site)
class ManagerProductAdmin(admin.ModelAdmin):
    fields = ("name", "art", "price", "count")
    list_display = ("name", "art", "price", "count")
    list_filter = ("category",)
    list_editable = ("price", "count")

@admin.register(Product, site=warehouse_site)
class WarehouseProductAdmin(admin.ModelAdmin):
    fields = ("name", "art", "price", "count")
    list_display = ("name", "art", "price", "count")
    list_filter = ("category",)
