import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import AccountFacebook

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("text_data la == ", text_data)
        text_data_json = json.loads(text_data)
        action = int(text_data_json['action'])
        if action != 7:
            fbid = text_data_json['facebook_id']
        else:
            fbid = ""
        data = {
            'type': 'chat_message',
            'type_control': 2,
            'app': 1,
            'action': action,
            'facebook_id': fbid
        }

        if action == 4:
            cookie = text_data_json['cookie']
            data['data'] = {
                    'cookie': cookie
            }

        if action == 1:
            id_post = text_data_json['id_post']
            data['data'] = {
                'id_post': id_post
            }

        if action == 7:
            id_post = text_data_json['id_post']
            data['data'] = {
                'id_post': id_post
            }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )

    # Receive message from room group
    def chat_message(self, event):
        print("event la == ", event)
        fbid = event['facebook_id']
        data = {}

        action = event['action']
        if action == 4:
            cookie = event['data']['cookie']
            data = {'cookie': cookie}
        if action == 1:
            id_post = event['data']['id_post']
            data = {'id_post': id_post}

        if action == 7:
            list_account = AccountFacebook.objects.all()
            print("vao day")
            print(list_account)
            id_post = event['data']['id_post']

            for item in list_account:
                data = {'id_post': id_post, 'cookie': item.cookie}

                self.send(text_data=json.dumps({
                    'type_control': 2,
                    'app': 1,
                    'action': 1,
                    'facebook_id':  item.userid,
                    'data': data
                }))


        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type_control': 2,
            'app': 1,
            'action': action,
            'facebook_id': fbid,
            'data': data
        }))
