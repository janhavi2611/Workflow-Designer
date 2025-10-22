from django.contrib import admin
from app.models import TODO

@admin.register(TODO)
class TODOAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'category', 'due_date', 'date')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description', 'user__username')
