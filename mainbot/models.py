from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    raffle = models.IntegerField(default=0)
    prize = models.CharField(max_length=255,null=False,default='None')
    keys = models.IntegerField(default=0)
    line = models.BooleanField(default=False)
    google = models.BooleanField(default=False)
    tsmc = models.BooleanField(default=False)
    ettoday = models.BooleanField(default=False)
    kkcompany = models.BooleanField(default=False)
    nxp = models.BooleanField(default=False)
    micron = models.BooleanField(default=False)
    akatsuki = models.BooleanField(default=False)
    cathay = models.BooleanField(default=False)
    taiwancement = models.BooleanField(default=False)
    itsa = models.BooleanField(default=False)
    itsa2 = models.BooleanField(default=False)
    interact_1 = models.BooleanField(default=False)
    interact_2 = models.BooleanField(default=False)
    interact_3 = models.BooleanField(default=False)
    
    def __str__(self):
        return self.uid

class Token(models.Model):
    token = models.CharField(max_length=10,null=False,default='')
    used = models.BooleanField(default=False)
    company = models.CharField(max_length=255,null=False,default='')
    code = models.CharField(max_length=255,null=False,default='')
    def __str__(self):
        return self.token
class Raffle(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=False,default='')
    level = models.IntegerField(default=0)
