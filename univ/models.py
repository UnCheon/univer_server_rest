# -*- coding: utf-8 -*-


from django.db import models
from thumbs import ImageWithThumbsField
from django.template.defaultfilters import default
from univer import settings
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    nick = models.CharField(max_length=100, null=True, unique=True)
    def __unicode__(self):
        return '%s' % (self.name)
    def get_absolute_url(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100, null=False)
    nick = models.CharField(max_length=100, null=False)
    region = models.ForeignKey(Region)
    def __unicode__(self):
        co = self.region.name + ' - ' + self.name
        return '%s' % (self.name)
    def get_absolute_url(self):
        return self.name
    

class College(models.Model):
    name = models.CharField(max_length=100, null=False)
    nick = models.CharField(max_length=100, null=False)
    university = models.ForeignKey(University)    
    def __unicode__(self):
        co =  self.university.name+' - '+self.name
        return '%s' % (co)
    def get_absolute_url(self):
        return self.name

class Major(models.Model):
    name = models.CharField(max_length=100, null=False)
    nick = models.CharField(max_length=100, null=False)
    college = models.ForeignKey(College)
    def __unicode__(self):
        co = self.college.name +' - '+self.name
        return '%s' % (co)
    def get_absolute_url(self):
        return self.name
    
class CustomUser(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    login_key = models.CharField(max_length=100, null=True, blank=True)    
    #other fields here
    # device 1.iphone 2.android 3.blackberry
    device_type = models.IntegerField()
    deviceToken = models.TextField()
    #university info
    region = models.ForeignKey(Region)
    university = models.ForeignKey(University)
    college = models.ForeignKey(College)
    def __unicode__(self):
        return '%s' % (self.user.username)
    def get_absolute_url(self):
        return self.user.username

    
class Book(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=80, null=False)
    original_price = models.CharField(max_length=80, null=False)
    discount_price = models.CharField(max_length=80, null=False)
    published = models.CharField(max_length=80, null=False)
    edition = models.CharField(max_length=10, null=False)
    publisher = models.CharField(max_length=80, null=False)
    book_author = models.CharField(max_length=80, null=False)
    content = models.TextField()
    region = models.ForeignKey(Region, null=True)
    university = models.ForeignKey(University, null=True)
    college = models.ForeignKey(College, null=True)
    image = ImageWithThumbsField(upload_to='documents/%Y/%m/%d', sizes=((50,50), (320,480)), null=True, blank=True)
    # 1:for sale 2:reserved 3:sold out
    sale = models.IntegerField()
    parcel = models.BooleanField()
    meet = models.BooleanField()
    # sale T purchase F
    isbn = models.CharField(max_length=20, null=True, blank=True)
    sell = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return '%s' % (self.title)
    def get_absolute_url(self):
        return self.title

    
    
class ChatRoom(models.Model): 
    user = models.ForeignKey(User, related_name='me')
    other_user = models.ForeignKey(User, related_name='you')
    last_message = models.CharField(max_length=100, null=True)
    edited = models.DateTimeField(auto_now_add = True, auto_now = True)
    # are you seller?
    seller = models.BooleanField()
    message_count = models.IntegerField(default=0)
    def __unicode__(self):
        return '%s' % (self.user.username)
    def get_absolute_url(self):
        return self.user.username


class Message(models.Model):
    seller_chatRoom = models.ForeignKey(ChatRoom, related_name='seller_chatRoom')
    buyer_chatRoom = models.ForeignKey(ChatRoom, related_name='buyer_chatRoom')
    seller = models.BooleanField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s' % (self.content)
    def get_absolute_url(self):
        return self.content
    
    
    
    
class Professor(models.Model):
    name = models.CharField(max_length=100, null=False)
    region = models.ForeignKey(Region)
    university = models.ForeignKey(University)
    college = models.ForeignKey(College)
    major = models.ForeignKey(Major, null=True, blank=True)
    image = ImageWithThumbsField(upload_to='professor/%Y/%m/%d', sizes=((50,50), (320,480)), null=True, blank=True)
    def __unicode__(self):
        return '%s' % (self.name)
    def get_absolute_url(self):
        return self.name

class Evaluation(models.Model):
    quality = models.FloatField(default=0)
    report = models.FloatField(default=0)
    grade = models.FloatField(default=0)
    personality = models.FloatField(default=0)
    attendance = models.FloatField(default=0)
    total = models.FloatField(default=0)
    like = models.SmallIntegerField(default=0)
    dislike = models.SmallIntegerField(default=0)
    count = models.SmallIntegerField(default=0)
    participant = models.ManyToManyField(User, null=True, blank=True)
    professor= models.OneToOneField(Professor, null=False, related_name='evaluation')
    comment_count = models.SmallIntegerField(default=0)
    def __unicode__(self):
        return '%s' % (self.professor.name)
    def get_absolute_url(self):
        return self.professor.name

    
class ProfessorComment(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    professor = models.ForeignKey(Professor)
    content = models.TextField()
    likeCount = models.SmallIntegerField(default=0, null=True, blank=True)
    dislikeCount = models.SmallIntegerField(default=0, null=True, blank=True)
    participant = models.ManyToManyField(User, null=True, blank=True, related_name='pParticipant')    
    def __unicode__(self):
        return '%s' % (self.content)
    def get_absolute_url(self):
        return self.content
    
    
class FreeBoard(models.Model):
    region = models.ForeignKey(Region)
    university = models.ForeignKey(University)
    def __unicode__(self):
        return '%s' % (self.university.name)
    def get_absolute_url(self):
        return self.university.name

class Entry(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    region = models.ForeignKey(Region)
    university = models.ForeignKey(University)
    created = models.DateTimeField(auto_now_add=True)
    image = ImageWithThumbsField(upload_to='entries/%Y/%m/%d', null=True, blank=True)
    commentCount = models.SmallIntegerField(default=0, null=True, blank=True)
    likeCount = models.SmallIntegerField(default=0, null=True, blank=True)
    dislikeCount = models.SmallIntegerField(default=0, null=True, blank=True)
    participant = models.ManyToManyField(User, null=True, blank=True, related_name='eParticipant')
    def __unicode__(self):
        return '%s' % (self.user.email)
    def get_absolute_url(self):
        return self.user.email


class EntryComment(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likeCount = models.SmallIntegerField(default=0, null=True, blank=True)
    dislikeCount = models.SmallIntegerField(default=0, null=True, blank=True)
    participant = models.ManyToManyField(User, null=True, blank=True, related_name='ecParticipant')
    def __unicode__(self):
        return '%s' % (self.user.email)
    def get_absolute_url(self):
        return self.user.email
    
    
    
    
    
    
########### WE PET MODELS

### WEPET
class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile_test')
    deviceName = models.CharField(max_length=100)
    deviceType = models.SmallIntegerField(null=False)
    pushKey = models.CharField(max_length=100, null=False, unique=True)
    
    
    
class Age(models.Model):
    age = models.SmallIntegerField()

class Species(models.Model):
    species = models.CharField(max_length=100, null=False, unique=True)
    sizeType = models.IntegerField()

class Dog(models.Model):
    name = models.CharField(max_length=100, null=False, unique=False)
    age = models.ForeignKey(Age)
    weight = models.FloatField()
    species = models.ForeignKey(Species)
    birthday = models.DateField()
    owner = models.ForeignKey(User, null=False)
    feeder = models.CharField(max_length=100, null=True)
    meter = models.CharField(max_length=100, null=True)
    tracker = models.CharField(max_length=100, null=True)




#### WE PET Meter


class HourData(models.Model):
    dog = models.ForeignKey(Dog)
    dateTime = models.DateTimeField(null=False)
    
    step1 = models.SmallIntegerField()
    step2 = models.SmallIntegerField()
    step3 = models.SmallIntegerField()
    step4 = models.SmallIntegerField()
    step5 = models.SmallIntegerField()
    step6 = models.SmallIntegerField()
    
    active = models.SmallIntegerField()
  
  
    
class DayData(models.Model):
    dog = models.ForeignKey(Dog)
    date = models.DateField()

    step = models.SmallIntegerField()
    active = models.SmallIntegerField()
    
    changeStep = models.SmallIntegerField()
    changActive = models.SmallIntegerField()
    
    stepStatus = models.BooleanField()
    activeStatus = models.BooleanField()
    
class WeekData(models.Model):
    dog = models.ForeignKey(Dog)
    startDate = models.DateField()
    endDate = models.DateField()
    
    step = models.SmallIntegerField()
    active = models.SmallIntegerField()
    
    changeStep = models.SmallIntegerField()
    changActive = models.SmallIntegerField()

    
    stepStatus = models.BooleanField()
    activeStatus = models.BooleanField()
    
class MonthData(models.Model):
    dog = models.ForeignKey(Dog)
    date = models.DateField()

    step = models.SmallIntegerField()
    active = models.SmallIntegerField()
    
    changeStep = models.SmallIntegerField()
    changActive = models.SmallIntegerField()
    
    stepStatus = models.BooleanField()
    activeStatus = models.BooleanField()
    
    

class AvgDogData(models.Model):    
    dog = models.ForeignKey(Dog)
    date = models.DateField()
    
    avgRecentStep = models.SmallIntegerField()
    avgRecentActive = models.SmallIntegerField()

class AvgSpeciseData(models.Model):
    species = models.ForeignKey(Species)
    date = models.DateField()
    
    avgDayStep = models.SmallIntegerField()
    avgWeekStep = models.SmallIntegerField()
    avgMonthStep = models.SmallIntegerField()
    
    avgDayActive = models.SmallIntegerField()
    avgWeekActive = models.SmallIntegerField()
    avgMonthActive = models.SmallIntegerField()
    

class AvgAgeData(models.Model):
    age = models.ForeignKey(Age) 
    date = models.DateField()

    avgDayStep = models.SmallIntegerField()
    avgWeekStep = models.SmallIntegerField()
    avgMonthStep = models.SmallIntegerField()
    
    avgDayActive = models.SmallIntegerField()
    avgWeekActive = models.SmallIntegerField()
    avgMonthActive = models.SmallIntegerField()

class AvgAllStep(models.Model):
    date = models.DateField()

    avgDayStep = models.SmallIntegerField()
    avgWeekStep = models.SmallIntegerField()
    avgMonthStep = models.SmallIntegerField()
    
    avgDayActive = models.SmallIntegerField()
    avgWeekActive = models.SmallIntegerField()
    avgMonthActive = models.SmallIntegerField()
    
    
class CleanDay(models.Model):
    dog = models.ForeignKey(Dog)
    startDate = models.DateField()
    cleanDay = models.SmallIntegerField()
    


#### GPS TAracker


class LocationLog(models.Model):
    dog = models.ForeignKey(Dog)
    dateTime = models.DateTimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    

class SafeZone(models.Model):
    dog = models.ForeignKey(Dog)
    homeLongitude = models.FloatField()
    homeLatitude = models.FloatField()
    range = models.FloatField()
    
class Activity(models.Model):
    dog = models.ForeignKey(Dog)
    dateTime = models.DateTimeField()
    distance = models.FloatField()
    time = models.FloatField()
    locationChange = models.TextField()
'''    위치변화를 제이슨형태 그대로 저장한다. ex) {{234232, 2324524}, {234232, 2324524}, {234232, 2324524},....., {234232, 2324524}, {234232, 2324524}} 
    Time을 예측할수 없기 때문에 텍스트형태로 저장하여 전송한다.
    
    
    activity의 월별 평균은 요일별 누적을  
''' 
    
    
class MonthActivity(models.Model):
    dog = models.ForeignKey(Dog)
    month = models.DateField()
    count = models.SmallIntegerField()

class ActivitySpeciesMonthAvg(models.Model):
    species = models.ForeignKey(Species)
    month = models.DateField()
    count = models.SmallIntegerField()
    
class ActivityAllMonth(models.Model):
    month = models.DateField()
    count = models.SmallIntegerField()
    

class ActivityAllFrequency(models.Model):
    monday = models.SmallIntegerField()
    tuesday = models.SmallIntegerField()
    wedneseday = models.SmallIntegerField()
    thursday = models.SmallIntegerField()
    friday = models.SmallIntegerField()
    saturday = models.SmallIntegerField()
    sunday = models.SmallIntegerField()

class ActivitySpeciseFrequency(models.Model):
    species = models.ForeignKey(Species)
    monday = models.SmallIntegerField()
    tuesday = models.SmallIntegerField()
    wedneseday = models.SmallIntegerField()
    thursday = models.SmallIntegerField()
    friday = models.SmallIntegerField()
    saturday = models.SmallIntegerField()
    sunday = models.SmallIntegerField()
    
    
    
#### WE PET Feeder





class DogFood(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    userCount = models.SmallIntegerField(default=0)
    
    moisture = models.FloatField()
    crudeProtein = models.FloatField()
    CrudeFat = models.FloatField()
    CrudeFiber = models.FloatField()
    CrudeAsh = models.FloatField(null=True, blank=True)
#    image = ImageWithThumbsField(upload_to='entries/%Y/%m/%d', null=True, blank=True)


class Feed(models.Model):
    dog = models.ForeignKey(Dog)
    lastFeedTime = models.DateTimeField()
    dogFood = models.ForeignKey(DogFood)
    
class FeedTracker(models.Model):
    dog = models.ForeignKey(Dog)
    eatStart = models.DateTimeField()
    eatEnd = models.DateTimeField()
    quantity = models.SmallIntegerField()    

    status = models.BooleanField()

#    20개의 점을 찍으며 1점당 15초 단위로 기록한다면 최대 5분까지 측정가
    s1 = models.SmallIntegerField(default=0)
    s2 = models.SmallIntegerField(default=0)
    s3 = models.SmallIntegerField(default=0)
    s4 = models.SmallIntegerField(default=0)
    
    s5 = models.SmallIntegerField(default=0)
    s6 = models.SmallIntegerField(default=0)
    s7 = models.SmallIntegerField(default=0)
    s8 = models.SmallIntegerField(default=0)
    
    s9 = models.SmallIntegerField(default=0)
    s10 = models.SmallIntegerField(default=0)
    s11 = models.SmallIntegerField(default=0)
    s12 = models.SmallIntegerField(default=0)
    
    s13 = models.SmallIntegerField(default=0)
    s14 = models.SmallIntegerField(default=0)
    s15 = models.SmallIntegerField(default=0)
    s16 = models.SmallIntegerField(default=0)
    
    s17 = models.SmallIntegerField(default=0)
    s18 = models.SmallIntegerField(default=0)
    s19 = models.SmallIntegerField(default=0)
    s20 = models.SmallIntegerField(default=0)
    

class FeedDayQuantity(models.Model):
    dog = models.ForeignKey(Dog)
    date = models.DateField()
    dayRecFeed = models.IntegerField()
    
    first = models.SmallIntegerField()
    second = models.SmallIntegerField(default=0)
    third = models.SmallIntegerField(default=0)
    fourth = models.SmallIntegerField(default=0)
    

class FeedAvg(models.Model):
    date = models.DateField()
    avgTime = models.CharField(max_length=100, null=False, blank=False)
    avgQuantity = models.CharField(max_length=100, null=False, blank=False)
    

class FeedSound(models.Model):
    dog = models.ForeignKey(Dog)
    file = models.FileField(upload_to='sounds/%Y/%m/%d', null=True, blank=True)
    
     