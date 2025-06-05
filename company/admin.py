from django.contrib import admin

from company.models import Company, Item


@admin.action(description="Очищает задолженность перед поставщиком")
def delete_debt(modeladmin, request, queryset):
    queryset.update(balance=0)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "city")
    actions = [delete_debt]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "mark")
    search_fields = ("name", "mark")
