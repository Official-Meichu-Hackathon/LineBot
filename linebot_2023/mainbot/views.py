from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

basic_list = ['FAQ','手冊','地圖','時程表','成果存放平台']



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text  #input
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url
                print(mtext)
                print(uid)
                print(name)
                print(pic_url)
                
                message=[]
                if mtext in basic_list:
                    match mtext:
                        case 'FAQ':
                            message.append(TextSendMessage(text='FAQ'))
                        case '手冊':
                            message.append(TextSendMessage(text='手冊'))
                        case '地圖':
                            message.append(TextSendMessage(text='地圖'))
                        case '時程表':
                            message.append(TextSendMessage(text='時程表'))
                        case '成果存放平台':
                            message.append(TextSendMessage(text='https://tenyear.meichuhackathon.org/'))


                
                
                
                
                line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()