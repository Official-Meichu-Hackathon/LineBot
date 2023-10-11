from django.shortcuts import render
from mainbot.models import *
# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

basic_list = ['FAQ','手冊','地圖','時程表','成果存放平台','企業博覽會規則']



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
                if User_Info.objects.filter(uid=uid).exists()==False:
                    print('iamnew')
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,points=0)
                    print(User_Info.objects.filter(uid=uid))
                message=[]
                if mtext in basic_list:
                    match mtext:
                        case 'FAQ':
                            message.append(TextSendMessage(text='我是常見問題'))
                        case '手冊':
                            message.append(TextSendMessage(text='https://tenyear.meichuhackathon.org/'))
                        case '地圖':
                            image_message = ImageSendMessage(
                                original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
                                preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
                            )
                            message.append(image_message)
                        case '時程表':
                            image_message = ImageSendMessage(
                                original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
                                preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
                            )
                            message.append(image_message)
                        case '成果存放平台':
                            message.append(TextSendMessage(text='https://tenyear.meichuhackathon.org/'))
                        case '企業博覽會規則':
                            message.append(TextSendMessage(text='****活動規則說明****\n1. afdsfadsf\n2. asdfasdfasdf\n3. asdfasdfasdf'))
                            message.append(TextSendMessage(text='****抽獎方法說明****\n1. afdsfadsf\n2. asdfasdfasdf\n3. asdfasdfasdf'))  
                elif mtext == '個人資訊':
                    userinfo = User_Info.objects.filter(uid=uid)
                    print(userinfo)
                    message.append(TextSendMessage(text='****抽獎方法說明****\n1. afdsfadsf\n2. asdfasdfasdf\n3. asdfasdfasdf'))  
                    #log in 
                else:
                    try:
                        key = token.objects.get(token=mtext)
                        user_info = User_Info.objects.get(uid=uid)
                        if key.used == True:
                            message.append(TextSendMessage(text='此序號已被使用過'))
                        elif getattr(user_info,key.company) == 1:
                            message.append(TextSendMessage(text='你已經有'+key.company+'的鑰匙了'))
                        else:
                            setattr(user_info,key.company,1)
                            key.used = True
                            user_info.keys += 1
                            key.save()
                            user_info.save()
                            message.append(TextSendMessage(text=f'恭喜你獲得{key.company}的鑰匙\n 您現在擁有{user_info.keys}把鑰匙'))
                    except:
                        message.append(TextSendMessage(text='功能暫不開放或請輸入正確指令'))
                line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()