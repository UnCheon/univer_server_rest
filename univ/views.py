# -*- coding: utf-8 -*-

# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from APNSWrapper import *
from pyapns import configure, provision, notify
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from feeds import *
from gcm import GCM
import json
import time, datetime



import unicodecsv
from cStringIO import StringIO

import md5

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
#from django.utils.encoding import force_str
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
#from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

import memcache
from locache import Locache


'''

@csrf_exempt    
def login(request):
    username=request.POST['username']
    password=md5.md5(request.POST['password']).hexdigest()
    password1=request.POST['password']
    try:
        user = User.objects.get(username=username)
        locache = Locache("127.0.0.1")
        result = locache.first_login(str(user.id))
        if result != 0:
            s=str(user.id)+'+'+result+'+'+user.first_name
            return HttpResponse(s)
        else:
            return HttpResponse('아이디와 비밀번호를 확인해 주세요')
    except:
        return HttpResponse('아이디와 비밀번호를 확인해 주세요')
        

@csrf_exempt
def login_check(request):
    key = request.POST['user_id']
    value = request.POST['value']
    locache = Locache()
    if locache.cache_login_check(str(key), str(value)) == True:
#        login success
        return HttpResponse('200')
    else:
#        login fail
        return HttpResponse('fail')




@csrf_exempt
def login2(request):
    password = md5.md5(request.POST['password']).hexdigest()
    user = User.objects.get(username=request.POST['username'], password=password)
    return HttpResponse(user.id)
    
    
@csrf_exempt
def logout(request):
    return HttpResponse('200')
'''        


@csrf_exempt
def testGCM(request):
    API_KEY = 'AIzaSyBIoZYJ1mOKB8x32svoYCqCSeS4yEhxbQM'
    gcm = GCM(API_KEY)
    data = {'title': '타이틀', 'content': '내용', 'ticker':'티'}

# Plaintext request
    reg_id = 'APA91bFFWd2KDbzx7I6amwY2GZBYF554kXqnd8VtApeqH7Iber0RuHY69VtEosUXvFENy6Oyr0T_SHT6mhbw4trrid_Jiti0wTDDP6jLKsWSejqjE0ytbrUTUu20rCK7nk9NoPLoA9yI'
    gcm.plaintext_request(registration_id=reg_id, data=data)

# JSON request
    reg_ids = ['APA91bFFWd2KDbzx7I6amwY2GZBYF554kXqnd8VtApeqH7Iber0RuHY69VtEosUXvFENy6Oyr0T_SHT6mhbw4trrid_Jiti0wTDDP6jLKsWSejqjE0ytbrUTUu20rCK7nk9NoPLoA9yI']
    response = gcm.json_request(registration_ids=reg_ids, data=data)
    return HttpResponse(response.success)
# Extra arguments
    res = gcm.json_request(
                           registration_ids=reg_id, data=data,
                           collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
                           )
    return HttpResponse(res)


@csrf_exempt
def testPOST(request):
    if request.method == 'POST':   
        postString = str(request.POST)
        firstCutString = postString[15:]
        reversedString = ''.join(reversed(firstCutString))
        secondCutString = reversedString[10:]
        secondReversedString = ''.join(reversed(secondCutString))
        data = json.loads(secondReversedString)
        
        return HttpResponse(data['content'])
    

@csrf_exempt
def makeDummy(request):
    region = Region.objects.get(id=1)
    a = 0
    universities = University.objects.filter(region=region)
    for university in universities:
        colleges = College.objects.filter(university=university)
        for college in colleges:
            a +=1
            title = 'test_book no'+str(a)
            Book.objects.create(user_id=request.POST['user_id'], title=title, original_price='25000', discount_price='14000', published='2012', edition='2', publisher='교학사',
                                   book_author='백운천', content='새책이에요', university=university, college=college, region=region, sale='1',
                                   parcel='1', meet='1', sell='1', isbn='12342')
            
            title = 'pro no'+str(a)
            
            professor = Professor.objects.create(name=title,
                                                 region=region,
                                                 university=university,
                                                 college=college,
                                                 major_id = 1,
#                                                 major=request.POST['major'],
                                                 )
            evaluation = Evaluation.objects.create(professor=professor, quality=0, report=0, grade=0, personality=0, attendance=0, total=0, count=0, like=0, dislike=0, comment_count=0)
    return HttpResponse('200')

def makeProfessorCommentsDummy(request):
    professor = Professor.objects.get(id=406)
    region = Region.objects.get(id=1)
    a = 0
    universities = University.objects.filter(region=region)
    for university in universities:
        colleges = College.objects.filter(university=university)
        for college in colleges:
            a +=1
            title = 'pro com no'+str(a)
            ProfessorComment.objects.create(user=request.POST['user_id'], professor=professor, content=title)
    return HttpResponse('200')


def professorEvaluate(request):
    professors = Professor.objects.all()
    for professor in professors:
        Evaluation.objects.create(professor=professor, quality=0, report=0, grade=0, personality=0, attendance=0, total=0, count=0, like=0, dislike=0, comment_count=0)
    return HttpResponse('200')


    
    

@csrf_exempt
def test(request):
    return render_to_response('test.html')
        


################# ACCOUNT    ######################


@csrf_exempt 
def login(request, template_name='registration/login.html',
          redirect_field_name='',
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """ 
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            
            netloc = urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponse('200')
                
#            return HttpResponseRedirect('success')
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return HttpResponse('아이디와 비밀번호가 맞지 않습니다.')




def logout(request, next_page=None,
          template_name='registration/logged_out.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          current_app=None, extra_context=None):
    return HttpResponse('200')
'''    
   """
   Logs out the user and displays 'You are logged out' message.
   """
   auth_logout(request)
   return HttpResponse('200')
   redirect_to = request.REQUEST.get(redirect_field_name, '')
   if redirect_to:
       netloc = urlparse(redirect_to)[1]
       # Security check -- don't allow redirection to a different host.
       if not (netloc and netloc != request.get_host()):
           return HttpResponseRedirect(redirect_to)

   if next_page is None:
       current_site = get_current_site(request)
       context = {
           'site': current_site,
           'site_name': current_site.name,
           'title': _('Logged out')
       }
       if extra_context is not None:
        else:
           context.update(extra_context)
       return TemplateResponse(request, template_name, context,
                               current_app=current_app)
       # Redirect to this page until the session has been cleared.
       return HttpResponseRedirect(next_page or request.path)
''' 

                                  
@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        password = md5.md5(request.POST['password']).hexdigest()
        university = University.objects.get(id=request.POST['university'])
        college = College.objects.get(id=request.POST['college'])
        region = Region.objects.get(id=request.POST['region'])
        deviceToken = request.POST['deviceToken']
        device_type = request.POST['device_type']
                                    
        try:
            User.objects.get(username=email)
            return HttpResponse('이미 존재하는 이메일 주소 입니다.')
        except:
            try:
                user = User.objects.create(username=email, email=email, password=password, first_name=first_name)
                try:
                    customUser = CustomUser.objects.create(user=user, device_type=device_type, deviceToken=deviceToken, university=university, college=college, region=region)
                    return HttpResponse('200')
                except:
                    user.delete()
                    return HttpResponse('커스텀유저 생성 오류. 관리자에게 문의하세요.')
            except:
                return HttpResponse('유저 생성 오류. 관리자에게 문의하세요.')
    elif request.method == 'PUT':
        return HttpResponse('put!')
    elif request.method == 'DELETE':
        return HttpResponse('delete!')



def nickname(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        user = User.objects.get(username=username)
        user.first_name = first_name
        user.save()
        return HttpResponse('200')
    elif request.method == 'PUT':
        return HttpResponse('put!')
    elif request.method == 'DELETE':
        return HttpResponse('delete!')



######### BOOKS  ######################


@csrf_exempt
def books(request):
    if request.method == 'POST':
        title = request.POST['title']
        original_price = request.POST['original_price']
        discount_price = request.POST['discount_price']
        published = request.POST['published']
        edition = request.POST['edition']
        publisher = request.POST['publisher']
        book_author = request.POST['book_author']
        content = request.POST['content']
        isbn = request.POST['isbn']
        
        university = University.objects.get(id=request.POST['university'])
        college = College.objects.get(id=request.POST['college'])
        region = Region.objects.get(id=request.POST['region'])
        if request.POST['parcel'] == '1':
            parcel = True
        else:
            parcel = False
            
        if request.POST['meet'] == '1':
            meet = True
        else:
            meet = False
            
        if request.POST['sell'] == '1':
            sell = True
        else:
            sell = False
             
        sale = request.POST['sale']
        
        try:
            image = request.FILES['image']
            book = Book.objects.create(user_id=request.POST['user_id'], title=title, original_price=original_price, discount_price=discount_price, published=published, edition=edition, publisher=publisher,
                                   book_author=book_author, content=content, university=university, college=college, region=region, image=image, sale=sale,
                                   parcel=parcel, meet=meet, sell=sell, isbn=isbn)
            return HttpResponse('200')
        except:
            book = Book.objects.create(user_id=request.POST['user_id'], title=title, original_price=original_price, discount_price=discount_price, published=published, edition=edition, publisher=publisher,
                                   book_author=book_author, content=content, university=university, college=college, region=region, sale=sale,
                                   parcel=parcel, meet=meet, sell=sell, isbn=isbn)
            return HttpResponse('200')
        
    elif request.method == 'PUT':
        sale = request.POST['sale']
        id = request.POST['id']
        book = Book.objects.get(id=id)
        book.sale = sale
        book.save()
        return HttpResponse('200')
    elif request.method == 'DELETE':
        id = request.POST['id']
        Book.objects.get(id=id).delete()
        return HttpResponse('200')
    elif request.method == 'GET':
        return HttpResponse('get요청입니다.')
    
         
    
@csrf_exempt
def myBooks(request):
    if request.user.is_authenticated():
        redirect_to = '/feeds/myentries/1/'
        return HttpResponseRedirect(redirect_to)
    else:
        return HttpResponse('100')


@csrf_exempt
def edit_books(request):
    sale = request.POST['sale']
    id = request.POST['id']
    book = Book.objects.get(id=id)
    book.sale = sale
    book.save()
    return HttpResponse('200')

@csrf_exempt
def delete_books(request):
    id = request.POST['id']
    book = Book.objects.get(id=id)
    book.delete()
    return HttpResponse('200')
    


############### Professors   ####################

@csrf_exempt
def professors(request):
    if request.method == 'POST':
        name = request.POST['name']
        region = int(request.POST['region'])
        university = int(request.POST['university'])
        college = int(request.POST['college'])
        
        try:
            image = request.FILES['image']
            professor = Professor.objects.create(name=name,
                                                 region_id=region,
                                                 university_id=university,
                                                 college_id=college,
                                                 major_id=1,
#                                                 major=request.POST['major'],
                                                 image = image,
                                                 )
            evaluation = Evaluation.objects.create(professor=professor, quality=0, report=0, grade=0, personality=0, attendance=0, total=0, count=0, like=0, dislike=0, comment_count=0)
            return HttpResponse('200')
        except:
            professor = Professor.objects.create(name=request.POST['name'],
                                                 region_id=region,
                                                 university_id=university,
                                                 college_id=college,
                                                 major_id = 1,
#                                                 major=request.POST['major'],
                                                 )
            evaluation = Evaluation.objects.create(professor=professor, quality=0, report=0, grade=0, personality=0, attendance=0, total=0, count=0, like=0, dislike=0, comment_count=0)
            return HttpResponse('200')
    elif request.method == 'PUT':
        return HttpResponse('put요청 입니다.')
    elif request.method == 'DELETE':
        return HttpResponse('delete요청 입니다.')
    
    
def professors_photo(request):
#    return HttpResponse('200')
    if request.method == 'POST':
        professor = Professor.objects.get(id=request.POST['professor_id'])
        image = request.FILES['image']
        professor.image = image
        professor.save() 
        return HttpResponse('200')
    elif request.method == 'PUT':
        return HttpResponse('put요청 입니다.')
    elif request.method == 'DELETE':
        return HttpResponse('delete요청 입니다.')


    
        
        
def evaluations(request):
    if request.method == 'POST':
        evaluation = Evaluation.objects.get(professor=request.POST['professor'])
        user = User.objects.get(id=request.POST['user_id'])
        for par in evaluation.participant.all():
            if user == par:
                return HttpResponse('이미 평가한 교수님 입니다. 다음학기에 다시 평가하세요~')
        
        evaluation.participant.add(user)
        evaluation.count += 1
       
        quality = float(request.POST['quality'])
        report = float(request.POST['report'])
        grade = float(request.POST['grade'])
        personality = float(request.POST['personality'])
        attendance = float(request.POST['attendance'])
        total = quality + report + grade + personality + attendance
        
        if request.POST['like'] == '1':
            like = 1
            dislike = 0
        else:
            like = 0
            dislike = 1
            
    
        evaluation.quality += quality
        evaluation.report += report 
        evaluation.grade += grade
        evaluation.personality += personality
        evaluation.attendance += attendance
        evaluation.like += like
        evaluation.dislike += dislike
        evaluation.total += total

        
        
        
        try:
            comment = request.POST['comment']
            professor = Professor.objects.get(id=request.POST['professor'])
            ProfessorComment.objects.create(professor=professor, content=comment, user_id=request.POST['user_id'])
            evaluation.comment_count += 1
            evaluation.save()
        except:
            evaluation.save()
        
        
        return HttpResponse('200')
        
    elif request.method == 'PUT':
        return HttpResponse('put요청입니다.')
    elif request.method == 'DELETE':
        return HttpRespose('delete요청 입니다.')
    elif request.method == 'GET':
        return HttpResponse('get요청 입니다.')
    

def comments_professors(request):
    if request.method == 'POST':
        professor = Professor.objects.get(id=request.POST['professor'])
        comment = request.POST['comment']
        ProfessorComment.objects.create(professor=professor, content=comment, user_id=request.POST['user_id'])
        professor.evaluation.comment_count += 1
        professor.evaluation.save()
        return HttpResponse('200')
    elif request.method == 'PUT':
        return HttpResponse('put!')
    elif request.method == 'DELETE':
        return HttpResponse('delete!!')
    
    

##################  MESSAGES   #############################


@csrf_exempt
def messages(request):
    if request.method == 'POST':
        postString = str(request.POST).encode("utf-8")
#        a = json.loads(request.POST)
#        return HttpResponse(a)
        
        
        
        firstCutString = postString[15:]
        reversedString = ''.join(reversed(firstCutString))
        secondCutString = reversedString[10:]
        secondReversedString = ''.join(reversed(secondCutString))
        data = json.loads(secondReversedString)
        other_user_id = data['other_user_id']
        user_id = data['user_id']
        content = data['content']
        sellerString = data['seller']
        
        
#        other_user_id = request.POST['other_user_id']
#        user_id = request.POST['user_id']
#        content = request.POST['content']
#        seller = request.POST['seller']
        
        
        if sellerString == '1':
            seller = True
            unseller = False
        else:
            seller = False
            unseller = True
        
        other_user = User.objects.get(id=other_user_id)
        user = User.objects.get(id=user_id)
        try:
            chatRoom = ChatRoom.objects.get(user=user, other_user=other_user, seller=seller)
        except:
            chatRoom = ChatRoom.objects.create(user=user, other_user=other_user, seller=seller)
        try:
            other_chatRoom = ChatRoom.objects.get(user=other_user, other_user=user, seller=unseller)
        except:
            other_chatRoom = ChatRoom.objects.create(user=other_user, other_user=user, seller=unseller)

        if seller == 1:
            Message.objects.create(seller_chatRoom=chatRoom, buyer_chatRoom=other_chatRoom, content=content, seller=1)
        else:
            Message.objects.create(seller_chatRoom=other_chatRoom, buyer_chatRoom=chatRoom, content=content, seller=0)
        chatRoom.message_count = 0
        chatRoom.last_message = content
        other_chatRoom.message_count += 1
        other_chatRoom.last_message = content
        chatRoom.save()
        other_chatRoom.save()
        pushMessage = user.first_name + ':' + content 
        if other_user.profile.device_type == 1:            
            configure({'HOST': 'http://localhost:7077/'})
            provision('univer', open('/home/projects/univer/univ/APNSWrapper/ck.pem').read(), 'sandbox')
            notify('univer', other_user.profile.deviceToken, {'aps':{'alert': pushMessage, 'badge': 10, 'sound': 'flynn.caf'}})
            return HttpResponse(str(chatRoom.id)) 
        elif other_user.profile.device_type == 2:
            API_KEY = 'AIzaSyBIoZYJ1mOKB8x32svoYCqCSeS4yEhxbQM'
            gcm = GCM(API_KEY)
            
#            uni_title = user.first_name.decode('utf-8')
            uni_content =  content.encode('utf-8')
            uni_name = user.first_name.encode('utf-8')
            ticker = uni_name + ':' + uni_content
#            return HttpResponse(type(uni_content)) 
#            ticker = user.first_name+':'+uni_content
#            return HttpResponse(type(ticker))
            data = {'title': uni_name, 'content': uni_content, 'ticker': ticker}
# Plaintext request
            reg_id = other_user.profile.deviceToken
            gcm.plaintext_request(registration_id=reg_id, data=data)
# JSON request
#            reg_ids = [reg_id]
#            response = gcm.json_request(registration_ids=reg_ids, data=data)
            return HttpResponse('200')
        elif other_user.profile.device_type == 3:
            return HttpResponse('blackberry')
    elif request.method == 'PUT':
            return HttpResponse('put 요청입니다')
    elif request.method == 'DELETE':
            return HttpResponse('DELETE 요청입니다.')
    elif request.method == 'GET':
        return HttpResponse('get요청입니다.')
    
    
    
    

@csrf_exempt
def chatRoomCheck(request):
    if request.method == 'POST':
        try:
            other_user = User.objects.get(id=request.POST['other_user_id'])
            chatRoom = ChatRoom.objects.get(user_id=int(request.POST['user_id']), other_user_id=int(request.POST['other_user_id']))
            chatRoom_id = str(chatRoom.id)
            return HttpResponse(chatRoom_id)
        except:
            return HttpResponse('0')
    elif request.method == 'PUT':
        return HttpResponse('put요청 입니다.')
    elif request.method == 'DELETE':
        return HttpResponse('delete요청 입니다.')
    elif request.method == 'GET':
        return HttpResponse('get요청 입니다.')
    
def chatRooms(request):
    if request.user.is_authenticated():
        redirect_to = '/feeds/chatRoom/'
        return HttpResponseRedirect(redirect_to)
    else:
        return HttpResponse('200')

    
@csrf_exempt
def entry(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            entry = Entry.objects.create(user_id=request.POST['user_id'], content=request.POST['content'], university_id=request.POST['university'], region_id=request.POST['region'], image=image, commentCount=0, likeCount=0, dislikeCount=0)
            return HttpResponse('200')
        except:
            entry = Entry.objects.create(user_id=request.POST['user_id'], content=request.POST['content'], university_id=request.POST['university'], region_id=request.POST['region'], commentCount=0, likeCount=0, dislikeCount=0)
            return HttpResponse('200')

    elif request.method == 'GET':
        return HttpResponse('get!')
    elif request.method == 'PUT':
        return HttpResponse('put!')
    elif request.method == 'DELETE':
        return HttpResponse('delete!')
    
    
@csrf_exempt
def entryLike(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=request.POST['user_id'])
            entry = Entry.objects.get(id=request.POST['id'])
            for par in entry.participant.all():
                if user == par:
                    return HttpResponse('좋아요는 한번만 누를 수 있습니다.')
            
            entry.likeCount += 1
            entry.participant.add(user)
            entry.save()
            return HttpResponse('200')
        except:
            return HttpResponse('Error 죄송합니다. 빠르게 해결하겠습니다.')
    elif request.method == 'GET':
        return HttpResponse('get!')
    elif request.method == 'PUT':
        return HttpResponse('put!')
    elif request.method == 'DELETE':
        return HttpResponse('delete!')

    
@csrf_exempt
def entryComment(request):
    if request.method == 'POST':
        entry = Entry.objects.get(id=request.POST['id'])
        EntryComment.objects.create(user_id=request.POST['user_id'], entry=entry, content=request.POST['content'])
        entry.commentCount += 1
        entry.save()
        return HttpResponse('200')
        return HttpResponse('Error 죄송합니다. 빠르게 해결하겠습니다.')
    elif request.method == 'GET':
        return HttpResponse('get!')
    elif request.method == 'PUT':
        return HttpResponse('put!')
    elif request.method == 'DELETE':
        return HttpResponse('delete!')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
####### past methods 
    
    
@csrf_exempt
def book_sale(request):
    sale = request.POST['sale']
    id = request.POST['id']
    book = Book.objects.get(id=id)
    book.sale = sale
    book.save()
    return HttpResponse('200')    

@csrf_exempt
def book_delete(request):
    id = request.POST['id']
    Book.objects.get(id=id).delete()
    return HttpResponse('200')

@csrf_exempt
def write_message(request):
    if request.method == 'POST':
        other_user_id = request.POST['other_user_id']
        user_id = request.POST['user_id']
        content = request.POST['content']
        seller = int(request.POST['seller'])
        if seller == 0:
            unseller = 1
        else:
            unseller = 0
        other_user = User.objects.get(id=other_user_id)
        user = User.objects.get(id=user_id)
        try:
            chatRoom = ChatRoom.objects.get(user=user, other_user=other_user, seller=seller)
        except:
            chatRoom = ChatRoom.objects.create(user=user, other_user=other_user, seller=seller)
        try:
            other_chatRoom = ChatRoom.objects.get(user=other_user, other_user=user, seller=unseller)
        except:
            other_chatRoom = ChatRoom.objects.create(user=other_user, other_user=user, seller=unseller)

        if seller == 1:
            Message.objects.create(seller_chatRoom=chatRoom, buyer_chatRoom=other_chatRoom, content=content, seller=1)
        else:
            Message.objects.create(seller_chatRoom=other_chatRoom, buyer_chatRoom=chatRoom, content=content, seller=0)
        chatRoom.message_count = 0
        chatRoom.last_message = content
        other_chatRoom.message_count += 1
        other_chatRoom.last_message = content
        chatRoom.save()
        other_chatRoom.save()
        if other_user.profile.device_type == 1:
            pushMessage = user.first_name + ':' + content 
            configure({'HOST': 'http://localhost:7077/'})
            provision('univer', open('/home/projects/univer/univ/APNSWrapper/ck.pem').read(), 'sandbox')
            notify('univer', other_user.profile.deviceToken, {'aps':{'alert': pushMessage, 'badge': 10, 'sound': 'flynn.caf'}})
            return HttpResponse(str(chatRoom.id)) 
        elif other_user.profile.device_type == 2:
            return HttpRespose('android')
        elif other_user.profile.device_type == 3:
            return HttpResponse('blackberry')
    elif request.method == 'PUT':
            return HttpResponse('put 요청입니다')
    elif request.method == 'DELETE':
            return HttpResponse('DELETE 요청입니다.')
    elif request.method == 'GET':
        return HttpResponse('get요청입니다.')

@csrf_exempt
def delete_chatRoom(request):
    chatRoom_id = request.POST['chatRoom_id']
    try:
        chatRoom = ChatRoom.objects.get(id=chatRoom_id)
        chatRoom.delete()
        return HttpResponse('200')
    except:
        return HttpResponse('201')



@csrf_exempt
def readMessage(request):
    chatRoom_id = request.POST['chatRoom_id']
    try:
        chatRoom = ChatRoom.objects.filter(id=chatRoom_id).update(message_count=0)
        return HttpResponse('100')
    except:
        return HttpResponse('101')


        