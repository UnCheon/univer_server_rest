from django.conf.urls.defaults import patterns, include, url
from univ.views import *
from univ.feeds import *
from univ.models import *
from django.contrib import admin
import os.path
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin

admin.autodiscover()
 
urlpatterns = patterns('',
                       
                       # test
                       (r'^testGCM/$', testGCM),
                       (r'^test/$', test),
                       (r'^testPOST/$', testPOST),
                       (r'^makeDummy/$', makeDummy),
                       (r'^makeProfessorCommentsDummy/$', makeProfessorCommentsDummy),
                       (r'^professorEvaluate/$', professorEvaluate),
                       
                       # Account
                       (r'^register/$', register),
                       (r'^login/$', login),
                       # (r'^login_check/$', login_check),
                       # (r'^login2/$', login2),
                       # (r'^logout/$', logout),
                       (r'^nickname/$', nickname),
                       
                       # Books
                       (r'^books/$', books),
                       (r'^feeds/books/search=(?P<search>\w+)&sale=(?P<sale>\w+)&category=(?P<category>\w+)&id=(?P<id>\w+)&page=(?P<page>\w+)/$', BooksFeed()),
                       (r'^myBooks/$', myBooks),
                       (r'^edit_books/$', edit_books),
                       (r'^delete_books/$', delete_books),
                       # Professors
                       (r'^professors/$', professors),
                       (r'^evaluations/$', evaluations),
                       (r'^comments/professor/$', comments_professors),
                       (r'^professors/photo/$', professors_photo),
                       (r'^evaluations/', evaluations),
                       (r'^feeds/professors/search=(?P<search>\w+)&category=(?P<category>\w+)&id=(?P<id>\w+)&page=(?P<page>\w+)/$', ProfessorFeed()),
                       (r'^feeds/comments/professor/professor_id=(?P<professor>\w+)&page=(?P<page>\w+)/$', ProfessorCommentsFeed()),
                       
                       # ChatRoom
                       (r'^chatRoomCheck/$', chatRoomCheck),
                       (r'^feeds/chatRooms/user_id=(?P<user_id>\w+)/$', ChatRoomsFeed()),
                       (r'^chatRooms/$', chatRooms),
                       (r'^chatRoom/delete/$', delete_chatRoom),
                       # Messages
                       (r'^messages/$', messages),
                       (r'^feeds/messages/chatRoom=(?P<chatRoom_id>\w+)&page=(?P<page>\w+)/$', MessagesFeed()),
                       # Entries
                       (r'^entry/$', entry),
                       (r'^like/entry/$', entryLike),
                       (r'^comments/entry/$', entryComment),
                       (r'^feeds/entries/category=(?P<category>\w+)&id=(?P<id>\w+)&page=(?P<page>\w+)/$', EntriesFeed()),
                       (r'^feeds/comments/entry/entry_id=(?P<entry>\w+)&page=(?P<page>\w+)/$', EntryCommentsFeed()),
                       
                       # Category
                       (r'^feeds/region/$', RegionFeed()),
                       (r'^feeds/univ/(?P<region_id>\w+)/$', UnivFeed()),
                       (r'^feeds/college/(?P<uni_id>\w+)/$', CollegeFeed()),
                       
                       # search ISBN 
                       (r'^feeds/searchisbnentries/(?P<sell>\w+)/(?P<isbn>\w+)/(?P<page>\w+)/$', SearchIsbnEntriesFeed()),
                       
                       # image
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),
                       # admin
                       (r'^admin/', include(admin.site.urls)),
                       
                       # login required
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        ############### past urls
#                       (r'^~ypunval/feeds/professors/(?P<search>\w+)/(?P<category>\w+)/(?P<id>\w+)/(?P<page>\w+)/$', ProfessorFeed()),
#                       (r'^~ypunval/feeds/books/(?P<search>\w+)/(?P<sale>\w+)/(?P<category>\w+)/(?P<id>\w+)/(?P<page>\w+)/$', BooksFeed()),
#                       
#                       (r'^~ypunval/book_sale/$', book_sale),
#                       (r'^~ypunval/book_delete/$', book_delete),
#                       
#                       
#                       (r'^~ypunval/write_message/$', write_message),
#                       (r'^~ypunval/read_message/$', readMessage),
#                       (r'^~ypunval/delete_chatRoom/$', delete_chatRoom),
#                       (r'^~ypunval/chatRoom_id/$', chatRoomCheck),
#                       
#                       
#                       # Book
#                       (r'^~ypunval/feeds/countryentries/(?P<sell>\w+)/(?P<page>\w+)/$', AllEntriesFeed()),
#                       (r'^~ypunval/feeds/regionentries/(?P<sell>\w+)/(?P<region_id>\w+)/(?P<page>\w+)/$', RegionEntriesFeed()),
#                       (r'^~ypunval/feeds/universityentries/(?P<sell>\w+)/(?P<uni_id>\w+)/(?P<page>\w+)/$', UnivEntriesFeed()),
#                       (r'^~ypunval/feeds/collegeentries/(?P<sell>\w+)/(?P<col_id>\w+)/(?P<page>\w+)/$', CollegeEntriesFeed()),
#                       (r'^~ypunval/feeds/sellerentries/(?P<user_id>\w+)/(?P<page>\w+)/$', SellerEntriesFeed()),
#                       (r'^~ypunval/feeds/myentries/(?P<page>\w+)/$', MyEntriesFeed()),
#                       
#                       # search Feeds 
#                       (r'^~ypunval/feeds/searchallentries/(?P<sell>\w+)/(?P<search>\w+)/(?P<page>\w+)/$', SearchAllEntriesFeed()),
#                       (r'^~ypunval/feeds/searchregionentries/(?P<sell>\w+)/(?P<region_id>\w+)/(?P<search>\w+)/(?P<page>\w+)/$', SearchRegionEntriesFeed()),
#                       (r'^~ypunval/feeds/searchunientries/(?P<sell>\w+)/(?P<uni_id>\w+)/(?P<search>\w+)/(?P<page>\w+)/$', SearchUniEntriesFeed()),
#                       (r'^~ypunval/feeds/searchcollentries/(?P<sell>\w+)/(?P<coll_id>\w+)/(?P<search>\w+)/(?P<page>\w+)/$', SearchCollEntriesFeed()),
#                       
#                       # message Feeds
#                       (r'^~ypunval/feeds/chatRooms/$', ChatRoomsFeed()),
#                       (r'^~ypunval/feeds/messages/(?P<chatRoom_id>\w+)/(?P<page>\w+)/$', MessagesFeed()),
    # Examples:
    # url(r'^$', 'unimajor.views.home', name='home'),
    # url(r'^unimajor/', include('unimajor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
