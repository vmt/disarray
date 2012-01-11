from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to
import settings

admin.autodiscover()

urlpatterns = patterns('',
    ('^$', 
        redirect_to, 
        {'url': '/t/', 'permanent': False}),
    (r'^t/', 
        include('disarray.task.urls', namespace="task")),
    (r'^login/$',
        'django.contrib.auth.views.login', 
        { 'template_name' : 'user_login.html' }),
    (r'^logout/$',
        'django.contrib.auth.views.logout'),
    (r'^admin/',
        include(admin.site.urls)),
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
        'django.views.static.serve', 
        { 'document_root' : settings.MEDIA_ROOT }),
)
