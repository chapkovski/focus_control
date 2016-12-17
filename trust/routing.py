from  otree.channels.default_routing import channel_routing
from channels.routing import route
from channels import Group
from .consumers import ws_message,ws_connect,ws_disconnect, ws_message_export,ws_connect_export,ws_disconnect_export
print('MAZAFAKA')
# print(default_routing)
channel_routing.extend((
    route("websocket.receive", ws_message_export,path=r'^/export/$'),
    route("websocket.connect", ws_connect_export,path=r'^/export/$'),
    route("websocket.disconnect", ws_disconnect_export,path=r'^/export/$'),

    route("websocket.receive", ws_message,path=r'^/chat/(?P<room>\w+)$'),
    route("websocket.connect", ws_connect,path=r'^/chat/(?P<room>\w+)$'),
    route("websocket.disconnect", ws_disconnect,path=r'^/chat/(?P<room>\w+)$'),
))
