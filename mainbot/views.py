from django.shortcuts import render
from mainbot.models import *
# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import re
from mainbot.admin_ids import admin_ids
from collections import defaultdict
import random
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

basic_list = ['FAQ','手冊','地圖','時程表','成果存放平台','企業博覽會規則','娛樂交流時間']
admin_list = ['梅竹黑客松開始抽獎','test','company distribute','user ratio']
company_list = [('akatsuki','曉數碼 Akatsuki Taiwan'),('cathay','國泰金控'),('ettoday','ETtoday新聞雲'),('google','Google'),('itsa','ITSA-易志偉教授'),('itsa2','ITSA-蕭宏章教授'),('kkcompany','科科科技（KKCompany Technologies）集團'),('line','LINE'),('micron','美光科技'),('nxp','恩智浦半導體與文曄科技'),('tsmc','台灣積體電路製造股份有限公司'),('taiwancement','台泥企業團'),('interact_1','就是不給泡'),('interact_2','星際大戰'),('interact_3','台灣有梭哈')]
award = ['🌱Level 1🌱\n-黑客松紀念T-shirt 25 件\n-精美大松帆布袋 50 個',
         '🌿Level 2🌿\n-100元健人餐折價券 50 張\n-筆電多功能吸盤折疊支架 1 組\n-記憶棉駝峰U型枕 1 組\n-304不鏽鋼雙飲口手提保溫瓶 1 個 \n-200元墊腳石網路折價券 10 張\n-鑄鐵鍋矽膠折折盒 4 組\n-有點麻購物袋–大ㄎ一ㄤ 6 張\n-威秀電影票券 3 張\n-統一超商100元禮券 24 張',
         '🌳Level 3🌳\n-無印良品USB桌上型風扇/低噪音/粉 1 臺\n-柯達M35 Film Camera 底片相機（薄荷綠）1 臺\n-M19雙層防燙不鏽鋼美食鍋1.2L-白木紋 1 組\n- Sony 立體聲耳罩式耳機 MDR-ZX110 1 副 \n-無線快充行動電源自帶線磁吸無線充 1 組\n-好提鈦瓷層保溫杯 1 個\n-GW 水玻璃經典2.0無線式迷你除濕機 1 臺']
key_need = [0,3,7,12]

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
                print(mtext,uid,name)
                user_info = User_Info.objects.filter(uid=uid)
                if user_info.exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                    print('create user with uid:'+uid+' name: '+name)
                    user_info = User_Info.objects.get(uid=uid)
                else:
                    user_info = user_info.first()
                message=[]
                if (mtext in admin_list) and (uid in admin_ids):# is admin
                    if mtext == '梅竹黑客松開始抽獎':
                        all_raffle = Raffle.objects.all()
                        raffles=[[],[],[]]
                        all_user = User_Info.objects.all()
                        for user in all_user: #reset
                            print(user.id, user.name, user.raffle, user.prize)    
                            user.prize = '參加獎🥲'
                            user.save()    
                        prizes = [
                            [],# no prize
                            ['精美大松帆布袋']*50+['黑客松紀念T-shirt']*75,
                            ['100元健人餐折價券']*50+['筆電多功能吸盤折疊支架']*1+['記憶棉駝峰U型枕']*1+['304不鏽鋼雙飲口手提保溫瓶']*1+['200元墊腳石網路折價券']*10+['鑄鐵鍋矽膠折折盒']*4+['有點麻購物袋–大ㄎ一ㄤ']*6+['威秀電影票券']*3+['統一超商100元禮券']*24,
                            ['MUJI USB桌上型風扇','柯達底片相機','雙層防燙不鏽鋼美食鍋','Sony立體聲耳罩式耳機','無線快充行動電源','GW水玻璃經典無線迷你除濕機']+['好提鈦瓷層保溫杯']*8,
                        ]
                        for i in range(4):
                            random.shuffle(prizes[i])
                        for raffle in all_raffle:
                            raffles[raffle.level].append(raffle.user_id) 
                        for i in range(4):
                            random.shuffle(raffles[i])
                        mes = 'success'
                        for i in range(3,0,-1):
                            random.shuffle(raffles[i])
                            for j in range(min(len(raffles[i]),len(prizes[i]))):
                                lucky_user = User_Info.objects.get(id=raffles[i][j])
                                lucky_user.prize = prizes[i][j]
                                lucky_user.save()
                                mes+=f'\nid:{lucky_user.id} name:{lucky_user.name} prize:{prizes[i][j]}'
                                print(f'id:{lucky_user.id} name:{lucky_user.name} prize:{prizes[i][j]}')
                            raffles[i-1]+=raffles[i][min(len(raffles[i]),len(prizes[i])):]
                        message.append(TextSendMessage(text=mes))
                    elif mtext=='test':
                        all_raffle = Raffle.objects.all()
                        all_user = User_Info.objects.all()
                        used_token = Token.objects.filter(used=True)
                        unused_token = Token.objects.filter(used=False)
                        for user in all_user:
                            print(user.id, user.name, user.raffle, user.prize,user.keys,user.line,user.google,user.tsmc,user.ettoday,user.kkcompany,user.nxp,user.micron,user.akatsuki,user.cathay,user.taiwancement,user.itsa,user.itsa2,user.interact_1,user.interact_2,user.interact_3)
                        for raffle in all_raffle:
                            print(raffle.user_id,raffle.name,raffle.level)
                        message.append(TextSendMessage(text=f'success {len(used_token)} {len(unused_token)}'))        
                    elif mtext == 'company distribute':
                        all_token = Token.objects.all()
                        count = defaultdict(int)
                        for token in all_token:
                            count[token.company]+=token.used
                        message.append(TextSendMessage(text=f'{count}'))
                    elif mtext == 'user ratio':
                        all_user_info_records = User_Info.objects.all()
                        ratio = defaultdict(int)
                        for user_info in all_user_info_records:
                            temp = 0
                            for (a,b) in company_list:
                                temp += getattr(user_info,a)
                            ratio[temp]+=1
                        message.append(TextSendMessage(text=f'{ratio}'))
                elif mtext in basic_list:
                    match mtext:
                        case 'FAQ':
                            message.append(TextSendMessage(text='✨ FAQ\nQ. 如果對於題目有疑問會有企業人員可以詢問嗎？\nA. 會喔！企業都將會有技術人員派駐在攤位上，歡迎有疑問的參賽者隨時去詢問他們～\n\nQ. 活動期間可以臨時離開會場嗎？\nA. 可以👌🏻\n\nQ.第一天活動時間\nA.第一天從8:00開始報到，活動會持續到22:00～沒有過夜喔\n\nQ.第二天簽到時間\nA.第二天8:00請各位參賽者記得來簽到喔，我們有準備早餐給大家🫶🏻\n\nQ. 會場內可以飲食嗎？\nA. 不行！體育館內嚴禁飲食！\n\nQ. 要怎麼參加抽獎？\nA. 只要將LINE Bot 轉換到企業博覽會頁面，參與並完成各擺攤企業之大會抽獎任務，獲得一組密碼並直接輸入於聊天室，即可獲得1支黑客鑰匙，集滿特定數量黑客鑰匙可參加各等級的抽獎！\n\n🌟 有其他問題也至服務台詢問工作人員！'))
                        case '手冊':
                            message.append(TextSendMessage(text='https://drive.google.com/file/d/1c_hMMvUPMXWPnVcKp12Wl44mmoK5Axdc/view'))
                        case '地圖':
                            # image_message = ImageSendMessage(
                            #     original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
                            #     preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
                            # )
                            # message.append(image_message)
                            continue
                        case '時程表':
                            # image_message = ImageSendMessage(
                            #     original_content_url=static('/time.png'),
                            #     preview_image_url=static('/time.png')
                            # )
                            # print('good')
                            # message.append(image_message)
                            continue
                        case '成果存放平台':
                            message.append(TextSendMessage(text='https://tenyear.meichuhackathon.org/'))
                        case '企業博覽會規則':
                            message.append(TextSendMessage(text="歡迎各位進入2023企業博覽會的抽獎活動🥰🎉\n🌟活動規則🌟\n1️⃣參加者完成企博攤位任務或參與指定娛樂交流\n2️⃣完成後即可向企業人員或關主領取密碼紙\n3️⃣將密碼輸入至 LINE Bot 聊天室\n4️⃣輸入後將顯示個人鑰匙累積總數\n\n📌一間企業 / 一個活動僅得一把鑰匙\n📌每個人的密碼皆不相同\n📌直接在聊天室輸入密碼即可\n📌密碼紙請拿至垃圾桶丟棄\n📌有任何問題歡迎詢問企博工作人員"))  
                            message.append(TextSendMessage(text='✨抽獎方法✨\n1️⃣在 LINE Bot 上按「兌換抽獎券」\n2️⃣選擇欲兌換的等級抽獎券\n（10/22（日）10:30 前都可以更動抽獎券等級）\n3️⃣10/22（日）將由工作人員統一抽獎\n4️⃣抽獎結果可於 10/22（日）11:00 後在「個人資訊」中查看\n\n🎟️抽獎時間：10/22（日）10:30 - 11:00\n🎟️領獎時間：10/22（日）11:00 - 13:30\n（如未於指定時間內領取獎品，將視為自動放棄中獎資格）\n\n📍一個人只有一張抽獎券\n📍詳細獎品請按「兌換抽獎券」➡️「查看 Level x 獎品」\n📍Level 3 可抽 Level 1 ~ 3 的獎品\n📍Level 2 可抽 Level 1 ~ 2 的獎品\n📍Level 1 可抽 Level 1 的獎品\n📍未中獎者可至抽獎台領取參加獎'))
                        case '娛樂交流時間':
                            # image_message = ImageSendMessage(
                            #     original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
                            #     preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
                            # )
                            # message.append(image_message)
                            continue
                elif mtext == '個人資訊':
                    raffle_temp = f'您有Level {user_info.raffle}  抽獎券'
                    if user_info.raffle == 0:
                        raffle_temp = '您還沒有抽獎券'
                    mes = f'您的名字：{user_info.name}\n您的序號： {user_info.id}\n您目前擁有鑰匙數： {user_info.keys}\n{raffle_temp}\n您抽到的獎品： {user_info.prize}\n您還需要以下鑰匙：\n'
                    for (a,b) in company_list:
                        if getattr(user_info,a) == 0:
                            mes+=b+'\n'
                    message.append(TextSendMessage(text=mes))  
                elif re.match(r"查看Level \d 抽獎券",mtext):
                    message.append(TextSendMessage(text=award[int(mtext[8])-1]))
                elif re.match(r"兌換Level \d 抽獎券",mtext):
                    addition = key_need[int(mtext[8])]
                    print(addition)
                    if addition+user_info.keys< int(key_need[int(mtext[8])]):
                        message.append(TextSendMessage(text=f'你的鑰匙不夠喔，需要 {key_need[int(mtext[8])]} 把鑰匙'))
                    else:
                        if user_info.raffle != 0:
                            raffle_record = Raffle.objects.get(user_id=user_info.id)
                            print(raffle_record)
                            raffle_record.delete()
                        user_info.raffle = int(mtext[8])
                        user_info.keys += addition
                        user_info.keys -= key_need[int(mtext[8])]
                        user_info.save()
                        Raffle.objects.create(user_id=user_info.id,name=user_info.name,level=int(mtext[8]))
                        message.append(TextSendMessage(text=f'恭喜您兌換Level {user_info.raffle} 抽獎券成功'))
                elif mtext == '兌換抽獎券':# since it will call the picture in linebot on developer setting we need not to use it
                    continue
                else:
                    print("no")
                    try:
                        key = Token.objects.get(token=mtext) 
                        print(key.used)
                        print(key.code)
                        print(getattr(user_info,key.code))
                        if key.used == True:
                            message.append(TextSendMessage(text='此序號已被使用過'))
                        elif getattr(user_info,key.code) == 1:
                            message.append(TextSendMessage(text='您已經有 '+key.company+' 的鑰匙了'))
                        else:
                            print("good")
                            setattr(user_info,key.code,1)
                            key.used = True
                            user_info.keys += 1
                            key.save()
                            user_info.save()
                            message.append(TextSendMessage(text=f'恭喜您獲得 {key.company} 的鑰匙\n 您現在擁有{user_info.keys}把鑰匙'))
                    except:
                        message.append(TextSendMessage(text='功能暫不開放或請輸入正確指令'))
                line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()