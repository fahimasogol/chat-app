# from channels.testing import WebsocketCommunicator
# from django.test import TestCase
# from config.routing import application  # Import your ASGI application
#
#
# class ChatConsumerTestCase(TestCase):
#     async def test_chat_consumer(self):
#         communicator = WebsocketCommunicator(application, "/ws/chat/room1/")
#         connected, subprotocol = await communicator.connect()
#         self.assertTrue(connected)
#
#         # Test sending text
#         await communicator.send_json_to({"message": "hello"})
#         response = await communicator.receive_json_from()
#         self.assertEqual(response, {"message": "hello"})
#
#         # Close
#         await communicator.disconnect()
