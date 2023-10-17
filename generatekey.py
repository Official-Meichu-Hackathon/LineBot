import random
import string
import collections
used = collections.defaultdict(bool)
begin ='LGTEKNMACWIiXYZ'
total_lists = [] 
def generate_city_code(length=5):
    characters = string.ascii_letters + string.digits  # 英數大小寫字符
    city_code = ''.join(random.choice(characters) for _ in range(length))
    while used[city_code]:
        city_code = ''.join(random.choice(characters) for _ in range(length))
    return city_code


f = open("openhouse_key.py",'w')
for be in begin:
    temp  = []
    for _ in range(500):
        temp.append(be + generate_city_code())
    print(be,'=',temp,file = f)
    total_lists.append(temp)
print('total_list','=',total_lists,file = f)

