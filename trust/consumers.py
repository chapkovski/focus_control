from channels import Group
import json
from channels.sessions import channel_session
from .models import Player, Focus
import random
from random import choice
from string import ascii_uppercase



@channel_session
def ws_message(message,room):

    print ("RAW MESSAGE"+message.content['text'])

    jsonmessage = json.loads(message.content['text'])
    whenhappens = str(jsonmessage['whenhappens'])
    whathappens = str(jsonmessage['whathappens'])
    wherehappens = str(jsonmessage['wherehappens'])
    print ('When shit happens:'+whenhappens)
    print ('What happens:'+whathappens)
    print ('Where shit happens:'+wherehappens)
    playerpk=str(jsonmessage['player'])
    myplayer = Player.objects.get(pk=playerpk)
    focus = myplayer.focus_set.create()    # create a new Decision object as part of the player's decision set
    focus.whenhappens = whenhappens
    focus.whathappens = whathappens
    focus.wherehappens = wherehappens
    print('success')
    focus.save()   # important: save to DB!
    # myfocuses = Focus.objects.get(player=playerpk)
    print(myplayer.participant.code)
    print ("-------")
    Group('export').send({'text': whathappens})

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
    Group("export").add(message.reply_channel)


# Connected to websocket.disconnect
def ws_disconnect(message,room):
    print("DISCONNECT MAZAFAKA!")
    Group("export").discard(message.reply_channel)

def ws_message_export(message):
    print ('export! message!!')


def ws_connect_export(message):
    Group("export").add(message.reply_channel)
    print ('export! connect!!')

def ws_disconnect_export(message):

    Group("export").discard(message.reply_channel)
    print ('export! disconnect!!')
