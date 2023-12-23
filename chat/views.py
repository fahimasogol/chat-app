from rest_framework import viewsets
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        if room_id:
            return ChatMessage.objects.filter(room=room_id)
        return ChatMessage.objects.none()  # Return empty queryset if room_id is not provided

    def create(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')
        if room_id:
            # Modify request data here if necessary
            return super().create(request, *args, **kwargs)
        # Handle invalid requests or provide a suitable response
