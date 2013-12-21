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

    url(r'^%s/dashboard/$' % (settings.PROJECT_NAME), 'dataui.views.dashboard', name = 'dashboard'),

    (r'^%s/static/(?P<path>.*)$' % (settings.PROJECT_NAME), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^reinforce/', include(admin.site.urls)),
)
