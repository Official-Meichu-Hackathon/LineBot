from django.shortcuts import render
from mainbot.models import *
# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import re

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

basic_list = ['FAQ','手冊','地圖','時程表','成果存放平台','企業博覽會規則']
company_list = ['AKATSUKI','CATHAY','ETTODAY','GOOGLE','ITSA','KKCOMPANY','LINE','MICRON','NXP','TSMC','TAIWANCEMENT','INTERACT_1','INTERACT_2','INTERACT_3']
award = ['1asdfasdfasdf','2asfasDFASDF','3dsFASDFASDF']
key_need = [3,7,12]
# line = models.BooleanField(default=False)
#     google = models.BooleanField(default=False)
#     tsmc = models.BooleanField(default=False)
#     ettoday = models.BooleanField(default=False)
#     kkcompany = models.BooleanField(default=False)
#     nxp = models.BooleanField(default=False)
#     micron = models.BooleanField(default=False)
#     akatsuki = models.BooleanField(default=False)
#     cathay = models.BooleanField(default=False)
#     taiwancement = models.BooleanField(default=False)
#     itsa = models.BooleanField(default=False)
#     interact_1 = models.BooleanField(default=False)
#     interact_2 = models.BooleanField(default=False)
#     interact_3 = models.BooleanField(default=False)

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
                user_info = User_Info.objects.filter(uid=uid)
                if user_info.exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,points=0)
                    print('create user with uid:'+uid+'name: '+name)
                    user_info = User_Info.objects.get(uid=uid)
                else:
                    user_info = user_info.first()
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
                    print(user_info.name)
                    print(user_info.id) 
                elif re.match(r"查看Level \d 抽獎券",mtext):
                    message.append(TextSendMessage(text=award[int(mtext[8])-1]))
                elif re.match(r"兌換Level \d 抽獎券",mtext):
                    if user_info.keys< int(key_need[int(mtext[8])-1]):
                        message.append(TextSendMessage(text=f'你的鑰匙不夠喔，需要 {key_need[int(mtext[8])-1]} 把鑰匙'))
                    elif user_info.raffle !=0:
                        message.append(TextSendMessage(text=f'你已經兌換過Level {user_info.raffle} 抽獎券了喔'))
                    else:
                        user_info.raffle = int(mtext[8])
                        user_info.keys -= key_need[int(mtext[8])-1]
                        user_info.save()
                        raffle.objects.create(user_id=user_info.id,name=user_info.name,level=int(mtext[8]))
                        message.append(TextSendMessage(text=f'恭喜你兌換Level {user_info.raffle} 抽獎券成功'))
                else:
                    try:
                        print('sorry')
                        key = token.objects.get(token=mtext)
                        print(key)
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