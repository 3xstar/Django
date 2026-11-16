from django.contrib import admin
from .models import Task, Category


# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'completed')
#     list_filter = ('completed',)
#     list_editable = ('completed',)

# нормальная реализация
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',) # поля для поиска

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed')  # поля для отображения

# admin.site.register(Task) простая реализация