import os
import django
# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linebot_2023.settings')  # 替換your_project為您的專案名稱
django.setup()
from mainbot.models import Token

import openhouse_key as data
# 寫入token資料
mapping = {'A': '曉數碼 Akatsuki Taiwan',
           'C': '國泰金控',
            'E': 'ETtoday新聞雲',
            'G': 'Google',
            'I': 'ITSA-易志偉教授',
            'i': 'ITSA-蕭宏章教授',
            'K': '科科科技（KKCompany Technologies）集團',
            'L': 'LINE',
            'M': '美光科技',
            'N': '恩智浦半導體與文曄科技',
            'T': '台灣積體電路製造股份有限公司',
            'W': '台泥企業團',
            'X': '活動一',
            'Y': '活動二',
            'Z': '活動三'}
           
def write_token_data():
    for keys in data.total_list:
        for key in keys:
            print(key,mapping[key[0]])
            Token.objects.create(token=key,company=mapping[key[0]])
        

if __name__ == '__main__':
    write_token_data()
