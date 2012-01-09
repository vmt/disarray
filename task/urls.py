from django.conf.urls.defaults import *

re_status_query = r'(?P<status_query>\w+([+]\w+)*)'
re_tag_query    = r'(?P<tag_query>\w+([+]\w+)*)'
re_order_by     = r'(?P<order_by>[-]?\w+)'

urlpatterns = patterns('',
    url(r'^$', 
            'disarray.task.views.list_tasks',
            name='main'),
    url(r'^add/$',
            'disarray.task.views.add',
            name='add'),
    url(r'^view/(?P<taskid>\d+)/$',
            'disarray.task.views.view',
            name='view'),
    url(r'^edit/(?P<taskid>\d+)/$',
            'disarray.task.views.edit',
            name='edit'),
    url('^search/$',
            'disarray.task.views.list_tasks',
            name='search'),
    url('^%s/$' % re_status_query,
            'disarray.task.views.list_tasks',
            name='list'),
    url('^%s/tagged/%s/$' % (re_status_query, re_tag_query),
            'disarray.task.views.list_tasks',
            name='list'),
    url('^%s/tagged/%s/%s/$' % (re_status_query, re_tag_query, re_order_by),
            'disarray.task.views.list_tasks',
            name='list'),
    url('^%s/%s/$' % (re_status_query, re_order_by),
            'disarray.task.views.list_tasks',
            name='list'),
    url(r'^remove/(?P<taskid>\d+)/$',
            'disarray.task.views.remove',
            name='remove'),
)
