from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^%s/$' % (settings.PROJECT_NAME), 'dataui.views.dashboard', name = 'dashboard'),
    
    url(r'^%s/logout/$' % (settings.PROJECT_NAME), 'dataui.views.user_logout', name = 'user_logout'),
    url(r'^%s/login/$' % (settings.PROJECT_NAME), 'dataui.views.user_login', name = 'user_login'),
    url(r'^%s/register/$' % (settings.PROJECT_NAME), 'dataui.views.register_user', name = 'register'),

    url(r'^%s/dashboard/$' % (settings.PROJECT_NAME), 'dataui.views.dashboard', name = 'dashboard'),

    url(r'^%s/news/(?P<news_id>\w+)/$' % (settings.PROJECT_NAME), 'dataui.views.news_details', name = 'news_details'),
    url(r'^%s/items/(?P<items_id>\w+)/$' % (settings.PROJECT_NAME), 'dataui.views.item_details', name = 'item_details'),
    url(r'^%s/items-requests/$' % (settings.PROJECT_NAME), 'dataui.views.items_request', name = 'items_request'),

    #url(r'^%s/itemsquestion/$' % (settings.PROJECT_NAME), 'dataui.views.pop_questions', name = 'pop_questions'),
    url(r'^%s/itemsanswer/$' % (settings.PROJECT_NAME), 'dataui.views.pop_answers', name = 'pop_answers'),

    url(r'^%s/addnews/$' % (settings.PROJECT_NAME), 'dataui.views.add_news', name = 'add_news'),
    url(r'^%s/editnews/(?P<news_id>\w+)/' % (settings.PROJECT_NAME), 'dataui.views.edit_news', name = 'edit_news'),

    url(r'^%s/additems/$' % (settings.PROJECT_NAME), 'dataui.views.add_item', name = 'add_item'),
    url(r'^%s/edit_items/(?P<items_id>\w+)/' % (settings.PROJECT_NAME), 'dataui.views.edit_items', name = 'edit_items'),

    (r'^%s/static/(?P<path>.*)$' % (settings.PROJECT_NAME), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^%s/display_img/(?P<path>.*)$' % (settings.PROJECT_NAME), 'django.views.static.serve', {'document_root': settings.IMAGE_ROOT}),
    
    url(r'^%s/about-us/$' % (settings.PROJECT_NAME), 'dataui.views.about_us', name = 'about_us'),
    
    # Uncomment the next line to enable the admin:
    (r'^%s/admin/' % (settings.PROJECT_NAME), include(admin.site.urls)),
)
