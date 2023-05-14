from django.db import models
from django.utils import timezone

# Create your models here.
class List(models.Model):
    DateTime = models.DateTimeField("案發日期") #案發時間
    Car = models.CharField(max_length = 10) #出勤車輛
    Detail = models.CharField(max_length = 10)  #內容(急病or車禍...)
    Location = models.CharField(max_length = 100)   #案發地點
    
class Record(models.Model):
    Active = models.CharField(max_length = 10) #行為
    IP = models.GenericIPAddressField() #用戶IP位置
    Content = models.CharField(max_length = 100) #內容
    Member = models.CharField(max_length = 10) #使用者
    DateTime = models.DateTimeField("Date modified", default=timezone.now) #紀錄時間