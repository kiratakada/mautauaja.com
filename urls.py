from django.conf.urls.defaults import *

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template
from mautauaja import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^%s/logout/$' % (settings.PROJECT_NAME), 'dataui.views.user_logout', name = 'user_logout'),
    url(r'^%s/login/$' % (settings.PROJECT_NAME), 'dataui.views.user_login', name = 'user_login'),
    url(r'^%s/register/$' % (settings.PROJECT_NAME), 'dataui.views.register_user', name = 'register'),

    url(r'^%s/dashboard/$' % (settings.PROJECT_NAME), 'dataui.views.dashboard', name = 'dashboard'),

    url(r'^%s/news/(?P<news_id>\w+)/$' % (settings.PROJECT_NAME), 'dataui.views.news_details', name = 'news_details'),
    url(r'^%s/items/(?P<items_id>\w+)/$' % (settings.PROJECT_NAME), 'dataui.views.item_details', name = 'item_details'),

    url(r'^%s/itemsquestion/$' % (settings.PROJECT_NAME), 'dataui.views.pop_questions', name = 'pop_questions'),
    url(r'^%s/itemsanswer/(?P<question_id>\w+)/$' % (settings.PROJECT_NAME), 'dataui.views.pop_answers', name = 'pop_answers'),

    url(r'^%s/itemprice/$' % (settings.PROJECT_NAME), 'dataui.views.pop_price', name = 'pop_price'),
    url(r'^%s/itemstore/$' % (settings.PROJECT_NAME), 'dataui.views.pop_store', name = 'pop_store'),
    url(r'^%s/storerate/(?P<store_id>\w+)/$' % (settings.PROJECT_NAME), 'dataui.views.store_rate', name = 'store_rate'),

    (r'^%s/static/(?P<path>.*)$' % (settings.PROJECT_NAME), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^%s/display_img/(?P<path>.*)$' % (settings.PROJECT_NAME), 'django.views.static.serve', {'document_root': settings.IMAGE_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^reinforce/', include(admin.site.urls)),
)
