"""for editing http://localhost:8000/admin page"""

from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message

admin.site.site_header = "Admin Area"
admin.site.site_title = "Admin Area"
admin.site.index_header = "index header?"


admin.site.register(Room)
# admin.site.register(Topic)
admin.site.register(Message)
# tabular inline


class RoomInLine(admin.TabularInline):
    """controls the (extra)number of rows of (model)rooms to add at once"""

    model = Room
    extra = 3


class TopicAdmin(admin.ModelAdmin):
    """shows number of editable fields in Topics"""

    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    inlines = [RoomInLine]


admin.site.register(Topic, TopicAdmin)
