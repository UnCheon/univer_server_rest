# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from models import *
from django.utils import feedgenerator
from django.utils.feedgenerator import Rss201rev2Feed
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



class CustomFeedUniv(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedUniv, self).add_item_elements(handler, item)
        handler.addQuickElement(u"book_count", item['book_count'])
        handler.addQuickElement(u"id", item['id'])
        handler.addQuickElement(u"nick", item['nick'])

class CustomFeedProfessor(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedProfessor, self).add_item_elements(handler, item)
        handler.addQuickElement(u"quality", item['quality'])
        handler.addQuickElement(u"report", item['report'])
        handler.addQuickElement(u"grade", item['grade'])
        handler.addQuickElement(u"attendance", item['attendance'])
        handler.addQuickElement(u"personality", item['personality'])
        handler.addQuickElement(u"total", item['total'])        
        handler.addQuickElement(u"count", item['count'])
        handler.addQuickElement(u"like", item['like'])
        handler.addQuickElement(u"dislike", item['dislike'])
        handler.addQuickElement(u"comment_count", item['comment_count'])   
        handler.addQuickElement(u"region", item['region'])        
        handler.addQuickElement(u"university", item['university'])
        handler.addQuickElement(u"college", item['college'])
        handler.addQuickElement(u"major", item['major'])                
        handler.addQuickElement(u"thumbnail", item['thumbnail'])
        handler.addQuickElement(u"image", item['image'])
        handler.addQuickElement(u"id", item['id'])


class CustomFeedBook(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedBook, self).add_item_elements(handler, item)
        handler.addQuickElement(u"seller_id", item['seller_id'])
        handler.addQuickElement(u"seller_nick", item['seller_nick'])
        handler.addQuickElement(u"title", item['title'])
        handler.addQuickElement(u"original_price", item['original_price'])
        handler.addQuickElement(u"discount_price", item['discount_price'])
        handler.addQuickElement(u"published", item['published'])
        handler.addQuickElement(u"edition", item['edition'])
        handler.addQuickElement(u"book_author", item['book_author'])
        handler.addQuickElement(u"edition", item['edition'])
        handler.addQuickElement(u"publisher", item['publisher'])
        handler.addQuickElement(u"thumbnail", item['thumbnail'])
        handler.addQuickElement(u"image", item['image'])
        handler.addQuickElement(u"parcel", item['parcel'])
        handler.addQuickElement(u"meet", item['meet'])
        handler.addQuickElement(u"sell", item['sell'])
        handler.addQuickElement(u"university", item['university'])
        handler.addQuickElement(u"college", item['college'])
        handler.addQuickElement(u"region", item['region'])
        handler.addQuickElement(u"sale", item['sale'])
        handler.addQuickElement(u"id", item['id'])
        handler.addQuickElement(u"created", item['created'])
        handler.addQuickElement(u"edited", item['edited'])
        handler.addQuickElement(u"isbn", item['isbn'])
        
        
class CustomFeedMessage(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedMessage, self).add_item_elements(handler, item)
        handler.addQuickElement(u"seller", item['seller'])

    
        
        
class CustomFeedChatRoom(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedChatRoom, self).add_item_elements(handler, item)
        handler.addQuickElement(u"seller", item['seller'])
        handler.addQuickElement(u"from_id", item['from_id'])
        handler.addQuickElement(u"to_id", item['to_id'])
        handler.addQuickElement(u"edited", item['edited'])
        handler.addQuickElement(u"count", item['count'])
        handler.addQuickElement(u"chatRoom_id", item['chatRoom_id'])
        
class CustomFeedEntry(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedEntry, self).add_item_elements(handler, item)
        handler.addQuickElement(u"region", item['region'])
        handler.addQuickElement(u"university", item['university'])
        handler.addQuickElement(u"created", item['created'])
        handler.addQuickElement(u"id", item['id'])
        handler.addQuickElement(u"like", item['like'])
        handler.addQuickElement(u"comment", item['comment'])
        handler.addQuickElement(u"image", item['image'])        
        
class CustomFeedEntryComments(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedEntryComments, self).add_item_elements(handler, item)
        handler.addQuickElement(u"created", item['created'])
        handler.addQuickElement(u"id", item['id'])                

        
        

class RegionFeed(Feed):
    feed_type = CustomFeedUniv
    title = u'Region'
    link = '/feeds/region/'
    description = u'대학교'
    def get_object(self, request):
        return Region.objects.all()
    def item_title(self, item):
        return item.name
    def item_description(self, item):
        return item.nick
    def item_extra_kwargs(self, item):
        return{
               'book_count':item.name,
               'id':str(item.id),
               'nick':item.nick,
               }
    def items(self, univ):
        return univ



class UnivFeed(Feed):
    feed_type = CustomFeedUniv
    title = u'University'
    link = '/feeds/univ/'
    description = u'대학교'
    def get_object(self, request, region_id):
        return University.objects.select_related().filter(region=int(region_id))
    def item_title(self, item):
        return item.name
    def item_description(self, item):
        return item.nick
    def item_extra_kwargs(self, item):
        return{
               'book_count':item.name,
               'id':str(item.id),
               'nick':item.nick,
               }
    def items(self, univ):
        return univ


class CollegeFeed(Feed):
    feed_type = CustomFeedUniv
    title = u'College'
    link = '/feeds/college/'
    description = u'대학교'
    def get_object(self, request, uni_id):
        return College.objects.select_related().filter(university=int(uni_id))
    def item_title(self, item):
        return item.name
    def item_description(self, item):
        return item.university.name
    def item_extra_kwargs(self, item):
        return{
               'book_count':item.name,
               'id':str(item.id),
               'nick':item.nick, 
               }
    def items(self, college):
        return college


class BooksFeed(Feed):
    feed_type = CustomFeedBook
    title = u'books'
    link = '/feeds/books/'
    description = u'books'
    def get_object(self, request, search, sale, category, id, page):
        start_pos = (int(page) - 1) * 30
        end_pos = start_pos + 30
        if sale == '0':
            sell = False
        else:
            sell = True
            
        if search == '1':
            return Book.objects.select_related().order_by('-created')[start_pos:end_pos]
            return books
        else:
            if category == '0':
                books=Book.objects.select_related().filter(sell=sell).order_by('-created')[start_pos:end_pos]
                return books
            elif category == '1':
                books=Book.objects.filter(sell=sell, region=id).order_by('-created')[start_pos:end_pos]
                return books
            elif category == '2':
                books=Book.objects.filter(sell=sell, university=id).order_by('-created')[start_pos:end_pos]
                return books
            elif category == '3':
                books=Book.objects.filter(sell=sell, college=int(id)).order_by('-created')[start_pos:end_pos]
                return books
            elif category == '4':
                books=Book.objects.filter(sell=sell, major=id).order_by('-created')[start_pos:end_pos]
                return books
            elif category == '5':
                books=Book.objects.filter(user=int(id))[start_pos:end_pos]
                return books
            elif category == '6':
                books=Book.objects.filter(user=int(id))[start_pos:end_pos]
                return books
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.content
    def item_author(self, item):
        return item.user.first_name
    def item_pubdate(self, item):
        return item.created
    def item_extra_kwargs(self, item):
        if item.parcel:
            parcel = '1'
        else:
            parcel = '0'
        if item.meet:
            meet = '1'
        else:
            meet = '0'
        if item.sell:
            sell = '1'
        else:
            sell = '0'
        return{
               'seller_id':str(item.user.id),
               'seller_nick':item.user.first_name,
               'original_price':item.original_price,
               'discount_price':item.discount_price,
               'published':item.published,
               'edition':item.edition,
               'publisher':item.publisher,
               'book_author':item.book_author,
               'thumbnail':item.image.url_50x50,
               'image':item.image.url_320x480,
               'parcel':parcel,
               'sale':str(item.sale),
               'meet':meet,
               'sell':sell,
               'university':item.university.nick,
               'college':item.college.nick,
               'region':item.region.name,       
               'id':str(item.id),        
               'created':str(item.created),
               'edited':str(item.edited),
               'isbn':item.isbn,
               }
    def items(self, book):
        return book



class SearchIsbnEntriesFeed(Feed):
    feed_type = CustomFeedBook
    title = u'Search ISBN Eintries'
    link = '/feeds/entries/'
    description = u'Entries'
    def get_object(self, request, sell, isbn, page):
        start_pos = (int(page) - 1) * 20
        end_pos = start_pos + 20
        return Book.objects.select_related().filter(sell=sell, isbn=isbn).order_by('-created')[start_pos:end_pos]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.content
    def item_author(self, item):
        return item.user.first_name
    def item_pubdate(self, item):
        return item.created
    def item_extra_kwargs(self, item):
        if item.parcel:
            parcel = '1'
        else:
            parcel = '0'
        if item.meet:
            meet = '1'
        else:
            meet = '0'
        if item.sell:
            sell = '1'
        else:
            sell = '0'
        return{
               'seller_id':str(item.user.id),
               'seller_nick':item.user.first_name,
               'original_price':item.original_price,
               'discount_price':item.discount_price,
               'published':item.published,
               'edition':item.edition,
               'publisher':item.publisher,
               'book_author':item.book_author,
               'thumbnail':item.image.url_50x50,
               'image':item.image.url_320x480,
               'parcel':parcel,
               'sale':str(item.sale),
               'meet':meet,
               'sell':sell,
               'university':item.university.nick,
               'college':item.college.nick,
               'region':item.region.name,
               'id':str(item.id),
               'created':str(item.created),            
               'edited':str(item.edited),
               'isbn':item.isbn,   
               }
    def items(self, book):
        return book



class ProfessorFeed(Feed):
    feed_type = CustomFeedProfessor
    title = u'교수피드'
    link = '/feeds/professor/'
    description = u'Professor'
    def get_object(self, request, search, category, id, page):
        start_pos = (int(page) - 1) * 30
        end_pos = start_pos + 30
        if search == '1':
            return Professor.objects.select_related().order_by('-id')[start_pos:end_pos]
        else:
            if category == '0':
                professors=Professor.objects.select_related().all().order_by('-id')[start_pos:end_pos]
                return professors
            elif category == '1':
                professors=Professor.objects.filter(region=id).order_by('-id')[start_pos:end_pos]
                return professors
            elif category == '2':
                professors=Professor.objects.filter(university=id).order_by('-id')[start_pos:end_pos]
                return professors
            elif category == '3':
                professors=Professor.objects.filter(college=id).order_by('-id')[start_pos:end_pos]
                return professors
            elif category == '4':
                professors=Professor.objects.filter(major=id).order_by('-id')[start_pos:end_pos]
                return professors
#        return Professor.objects.select_related().all()
    def item_title(self, item):
        return item.name
    def item_description(self, item):
        return str(item.evaluation.total)
    def item_extra_kwargs(self, item):
        count = item.evaluation.count
        return{
               'quality':str(item.evaluation.quality),
               'report':str(item.evaluation.report),
               'grade':str(item.evaluation.grade),
               'attendance':str(item.evaluation.attendance),
               'personality':str(item.evaluation.personality),
               'total':str(item.evaluation.total),
               'count':str(item.evaluation.count),
               'like': str(item.evaluation.like),
               'dislike': str(item.evaluation.dislike),
               'comment_count':str(item.evaluation.comment_count),
               'region':item.region.name,
               'university':item.university.nick,
               'college':item.college.nick,
               'major':'임시',
               'thumbnail':item.image.url_50x50,
               'image':item.image.url_320x480,
               'id':str(item.id),
               }
    def items(self, professor):
        return professor

class ProfessorCommentsFeed(Feed):
    feed_type = CustomFeedEntryComments
    title = u'교수평가 댓글 피드'
    link = '/feeds/professors/comments/id=&page=/'
    description = u'professors comments'
    def get_object(self, request, professor, page):
        start_pos = (int(page) - 1) * 30
        end_pos = start_pos + 30        
        return ProfessorComment.objects.select_related().filter(professor=int(professor)).order_by('-id')[start_pos:end_pos]
    def item_title(self, item):
        return item.user.first_name
    def item_description(self, item):
        return item.content
    def item_pubdate(self, item):
        return item.created
    def item_extra_kwargs(self, item):
        return{
               'created':str(item.created),
               'id':str(item.id),
               }

    def items(self, comment):
        return comment



    
class ChatRoomsFeed(Feed):
    feed_type = CustomFeedChatRoom
    title = u'채팅리스트'
    link = '/feeds/entries/'
    description = u'Entries'
    def get_object(self, request, user_id):
        return ChatRoom.objects.select_related().filter(user_id=user_id).order_by('-edited')
    def item_title(self, item):
        return item.other_user.first_name
    def item_description(self, item):
        return item.last_message
    def item_pubdate(self, item):
        return item.edited
    def item_extra_kwargs(self, item):
        if item.seller:
            seller = '1'
        else:
            seller = '0'
        return{
               'seller':seller,
               'to_id':str(item.other_user.id),
               'from_id':str(item.user.id),
               'edited':str(item.edited),
               'count':str(item.message_count),
               'chatRoom_id':str(item.id),
               }
    def items(self, chatRoom):
        return chatRoom

 
class MessagesFeed(Feed):
    feed_type = CustomFeedMessage
    title = u'메세지피드'
    link = '/feeds/entries/'
    description = u'Entries'
    def get_object(self, request, chatRoom_id, page):
        start_pos = (int(page) - 1) * 30
        end_pos = start_pos + 30        
        return Message.objects.select_related().filter(Q(seller_chatRoom=int(chatRoom_id)) | Q(buyer_chatRoom=int(chatRoom_id))).order_by('-created')[start_pos:end_pos]
    def item_title(self, item):
        return item.seller_chatRoom.user.first_name
    def item_description(self, item):
        return item.content
    def item_pubdate(self, item):
        return item.created
    def item_extra_kwargs(self, item):
        if item.seller:
            seller = '1'
        else:
            seller = '0'
        return{
               'seller':seller,
               }
    def items(self, message):
        return message
    

class EntriesFeed(Feed):
    feed_type = CustomFeedEntry
    title = u'글피'
    link = '/feeds/entries/'
    description = u'Entries'
    def get_object(self, request, category, id, page):
        start_pos = (int(page) - 1) * 30
        end_pos = start_pos + 30        
        if category == '0':
            return Entry.objects.select_related().all().order_by('-id')[start_pos:end_pos]
        elif category == '1':
            return Entry.objects.select_related().filter(region=id).order_by('-id')[start_pos:end_pos]
        elif category == '2':
            return Entry.objects.select_related().filter(university=id).order_by('-id')[start_pos:end_pos]
    def item_title(self, item):
        return item.user.first_name
    def item_description(self, item):
        return item.content
    def item_pubdate(self, item):
        return item.created
    def item_extra_kwargs(self, item):
        return{
               'region':item.region.name,
               'university':item.university.nick,
               'like':str(item.likeCount),
               'comment':str(item.commentCount),
               'created':str(item.created),
               'id':str(item.id),
               'image':str(item.image),
               }
    def items(self, entry):
        return entry
    

class EntryCommentsFeed(Feed):
    feed_type = CustomFeedEntryComments    
    title = u'교수평가 댓글 피드'
    link = '/feeds/entrycomments/entry_id=&page=/'
    description = u'professors comments'
    def get_object(self, request, entry, page):
        start_pos = (int(page) - 1) * 20
        end_pos = start_pos + 20        
        return EntryComment.objects.select_related().filter(entry=int(entry)).order_by('-id')[start_pos:end_pos]
    def item_title(self, item):
        return item.user.first_name
    def item_description(self, item):
        return item.content
    def item_pubdate(self, item):
        return item.created
    def item_extra_kwargs(self, item):
        return{
               'created':str(item.created),
               'id':str(item.id),
               }
    def items(self, comment):
        return comment
    



