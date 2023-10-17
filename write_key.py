import os
import django
# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linebot_2023.settings')  # 替換your_project為您的專案名稱
django.setup()
from mainbot.models import Token

import openhouse_key as data
# 寫入token資料
mapping = {'A': ('曉數碼 Akatsuki Taiwan','akatsuki'),
           'C': ('國泰金控','cathay'),
            'E': ('ETtoday新聞雲','ettoday'),
            'G': ('Google','google'),
            'I': ('ITSA-易志偉教授','itsa'),
            'i': ('ITSA-蕭宏章教授','itsa2'),
            'K': ('科科科技（KKCompany Technologies）集團','kkcompany'),
            'L': ('LINE','line'),
            'M': ('美光科技','micron'),
            'N': ('恩智浦半導體與文曄科技','nxp'),
            'T': ('台灣積體電路製造股份有限公司','tsmc'),
            'W': ('台泥企業團','taiwancement'),
            'X': ('就是不給泡','interact_1'),
            'Y': ('星際大戰','interact_2'),
            'Z': ('台灣有梭哈','interact_3'),
            }
def write_token_data():
    Token.objects.all().delete()
    for keys in data.total_list:
        total = 0;
        for key in keys:
            total+=1
            Token.objects.create(token=key,company=mapping[key[0]][0],code=mapping[key[0]][1] )
        print(total)

if __name__ == '__main__':
    write_token_data()
