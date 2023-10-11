import os
import django
# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linebot_2023.settings')  # 替換your_project為您的專案名稱
django.setup()
from mainbot.models import token

import openhouse_key as data


# 寫入token資料
mapping = {'L':'line',
                'G':'google',
                'T':'tsmc',
                'E':'ettoday',
                'K':'kkcompany',
                'N':'nxp',
                'M':'micron',
                'A':'akatsuki',
                'C':'cathay',
                'W':'taiwancement',
                'I':'itsa',
                'i':'itsa2',
                'X':'interact_1',
                'Y':'interact_2',
                'Z':'interact_3'
            }
def write_token_data():
    for keys in data.total_list:
        for key in keys:
            print(key,mapping[key[0]])
            token.objects.create(token=key,company=mapping[key[0]])
        

if __name__ == '__main__':
    write_token_data()
