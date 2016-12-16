from channels import Group
import json
from channels.sessions import channel_session
from .models import Player, Focus
import random
from random import choice
from string import ascii_uppercase


@channel_session
def ws_message(message,room):
    # print("MESSAGE MAZAFAKA!")
    # print(message.content['reply_channel'])
    # print(message.content['path'])
    # # print(message.content['bytes'])
    # print(message.content['text'])
    print ("RAW MESSAGE"+message.content['text'])
    jsonmessage = json.loads(message.content['text'])
    # print ('Curent page:'+jsonmessage['current_title'])
    # print ('Player ID:'+str(jsonmessage['player']))
    print ('When shit happens:'+str(jsonmessage['date']))
    print ('What happens:'+str(jsonmessage['status']))
    print ('Player PK:'+str(jsonmessage['player']))
    playerpk=str(jsonmessage['player'])
    myplayer = Player.objects.get(pk=playerpk)
    focus = myplayer.focus_set.create()    # create a new Decision object as part of the player's decision set
    focus.infocus = random.randint(1, 10)
    focus.timefocus = ''.join(choice(ascii_uppercase) for i in range(12))
    print('success')
    focus.save()   # important: save to DB!
    # myfocuses = Focus.objects.get(player=playerpk)
    print(myplayer.participant.code)
    print ("-------")
    focus_qs = Focus.objects.filter(player__exact=myplayer)
    for f in focus_qs:
        print(f.infocus)
    print ("-------")
    # print(message.content['order'])
    # print('END OF MESSAGE MAZAFAKA ==============')
    # text = message.content.get('text')
    # curpage = jsonmessage['current_title']
    # player = str(jsonmessage['player'])
    # date = str(jsonmessage['date'])
    # otreegroup = str(jsonmessage['otreegroup'])
    # if text:
    #     Group('chat').send({'text': json.dumps({'curpage': curpage,
    #                                             'player':player,
    #                                             'group':otreegroup,
    #                                             'date':date,
    #                                             'sender': message.reply_channel.name})})
    #

    # 'text': json.dumps({
    # 'message': message.content['text'],
    # 'sender': message.reply_channel.name})
    #
    # Group("chat").send({
    #         "text": "[user] %s" % (randint(0,9)),#message.content['text'],
    #     })

@channel_session
def ws_connect(message,room):
    print("CONNECT MAZAFAKA!!!!")
    Group("chat").add(message.reply_channel)


# Connected to websocket.disconnect
def ws_disconnect(message,room):
    print("DISCONNECT MAZAFAKA!")
    Group("chat").discard(message.reply_channel)
