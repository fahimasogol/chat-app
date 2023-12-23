# urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ChatRoomViewSet, ChatMessageViewSet
#
# router = DefaultRouter()
# router.register(r'chatrooms', ChatRoomViewSet)
# router.register(r'chatmessages/(?P<room_id>[^/.]+)', ChatMessageViewSet, basename='chatmessage')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
#
# urls.py
# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chatmessages/room/<int:room_id>/', ChatMessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='chatmessage-by-room'),
]

