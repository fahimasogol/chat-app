from django.contrib import admin
from .models import ChatRoom, ChatMessage


# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'timestamp')
    search_fields = ('room__name', 'user__username', 'message')
    ordering = ('-timestamp',)
