from  otree.channels.default_routing import channel_routing
from channels.routing import route
from channels import Group
from .consumers import ws_message,ws_connect,ws_disconnect
print('MAZAFAKA')
# print(default_routing)
channel_routing.extend((
    route("websocket.receive", ws_message,path=r'^/chat/(?P<room>\w+)$'),
    route("websocket.connect", ws_connect,path=r'^/chat/(?P<room>\w+)$'),
    route("websocket.disconnect", ws_disconnect,path=r'^/chat/(?P<room>\w+)$'),
))
