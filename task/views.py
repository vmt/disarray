from django import forms
from django.forms.widgets import TextInput, Textarea, CheckboxInput
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from disarray.task.models import Task, TaskUpdate, TASK_STATUS_CHOICES
from datetime import datetime

ORDERING_CHOICES = (
    ( "-views", 'Most Viewed' ),
    ( "-createdon", 'Most Recent' ),
    ( "views", 'Least Viewed' ),
    ( "createdon", 'Least Recent' ),
)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'text', 'tags')
        widgets = {
            'title' :  TextInput()
        }

class TaskUpdateForm(forms.Form):
    status = forms.ChoiceField(required=True, 
                               choices=TASK_STATUS_CHOICES)
    text = forms.CharField(widget=Textarea())

class TaskSearchForm(forms.Form):
    status = forms.MultipleChoiceField(required=False, 
               choices=TASK_STATUS_CHOICES)
    tags = forms.CharField()
    ordering = forms.ChoiceField(required=False, 
               choices=ORDERING_CHOICES)

@login_required
def main(request):
    return render_to_response('task/main.html',
                              context_instance=RequestContext(request)) 

@login_required
def add(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.modifiedon = datetime.now()
            task.viewedon = datetime.now()
            task.views = 1
            task.save()
            form.save_m2m()
            request.user.message_set.create(message="Task %d created" % task.id)
            return redirect("task:view", taskid=task.id)
    return render_to_response('task/task_form.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

@login_required
def edit(request, taskid):
    task = get_object_or_404(Task, pk=taskid)
    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.modifiedon = datetime.now()
            task.save()
            form.save_m2m() # .. because, tags
            request.user.message_set.create(message="Task %d updated" % task.id)
            return redirect("task:view", taskid=task.id)
    return render_to_response('task/task_form.html',
                              { 'task': task, 'form': form },
                              context_instance=RequestContext(request))


@login_required
def view(request, taskid):
    task = get_object_or_404(Task, pk=taskid)
    updates = task.taskupdate_set.all().order_by('createdon')
    if request.method == 'POST':
        update_form = TaskUpdateForm(request.POST)
        if update_form.is_valid():
            task.status = update_form.cleaned_data['status']
            if update_form.cleaned_data['text']:
                TaskUpdate.objects.create(task=task, 
                        text=update_form.cleaned_data['text'])
            task.save()
            request.user.message_set.create(message="Task %d updated" % task.id)
            return redirect("task:view", taskid=task.id)
    else:
        update_form = TaskUpdateForm(initial={'status' : task.status })
        task.viewedon = datetime.now()
        task.views += 1
        task.save()
    return render_to_response('task/view.html', 
                              { 'task' : task, 
                                'updates' : updates,
                                'update_form' : update_form }, 
                              context_instance=RequestContext(request))

def annotate_filters(all_filters, selected_filters):
    afilters = []
    for _f in  all_filters:
        f = unicode(_f)
        if f in selected_filters:
            slug = '+'.join([ str(t) for t in selected_filters if str(t) != f ])
        else:
            slug = '+'.join(selected_filters + [str(f)])
        afilters.append({ 
            'label'    : str(f),
            'selected' : True if f in selected_filters else False,
            'slug'     : slug })
    return afilters

class TaskFilter:
   
    def __init__(self, tags, statuses, order_by):
        self.tags = tags
        self.statuses = statuses
        self.order_by = order_by

    def get_url(self, tags, statuses, order_by):
        kwargs = {}
        if tags:
            kwargs['tag_query'] = '+'.join(tags)
        if statuses:
            kwargs['status_query'] = '+'.join(statuses)
        if order_by:
            kwargs['order_by'] = unicode(order_by)
        return reverse('task:list', kwargs=kwargs)

    def get_status_url(self, status): 
        kwargs = {}
        statuses = []
        if self.statuses:
            if status in self.statuses:
                statuses = filter(lambda t: t != status, self.statuses)
            else:
                statuses = self.statuses + [status]
        else:
            statuses = [status]
        if not statuses:
            statuses = ['all']
        return self.get_url(self.tags, statuses, self.order_by)

    def get_tag_url(self, tag): 
        kwargs = {}
        tags = []
        if self.tags:
            if tag in self.tags:
                tags = filter(lambda t: t != tag, self.tags)
            else:
                tags = self.tags + [tag]
        else:
            tags = [tag]
        return self.get_url(tags, self.statuses, self.order_by)

    def annotate_tag(self, tag):
        return ({
            'label'    : tag,
            'selected' : True if tag in self.tags else False,
            'url'      : self.get_tag_url(tag) })

    def annotate_status(self, status):
        return ({
            'label'    : status,
            'selected' : True if status in self.statuses else False,
            'url'      : self.get_status_url(status) })

@login_required
def list_tasks(request, status_query='new+open', 
                        tag_query=None,
                        order_by='-views',
                        page=0,
                        tasks_per_page=50):
    tags, statuses = [], []
    tasks = Task.objects.all()
    if status_query == 'all':
        status_query = '+'.join([ status for status, _ in TASK_STATUS_CHOICES ])
    statuses = (status_query).split('+')
    tasks = tasks.filter(status__in=status_query.split('+'))
    if tag_query is not None:
        tags = (tag_query).split('+')
        for tag in tag_query.split('+'):
            tasks = tasks.filter(tags__name__in=[tag]).distinct()
    tasks = tasks.order_by(order_by)[0:tasks_per_page]

    task_filter = TaskFilter(tags, statuses, order_by)

    task_list = []
    for task in tasks:
        task_list.append({ 
          'id'     : task.id,
          'title'  : task.title,
          'text'   : task.text,
          'status' : task.status,
          'tags'   : [ task_filter.annotate_tag(str(tag)) for tag in task.tags.all() ]
        })

    # send a list of status choices
    # send a list of order choices
    # send a list of tag choices

    all_tags = [ task_filter.annotate_tag(str(tag)) for tag in Task.tags.most_common() ]
    all_statuses = [ task_filter.annotate_status(status) for status, _ in TASK_STATUS_CHOICES ]

    return render_to_response('task/list.html',
                              { 'tasks'    : task_list, 
                                'tags'     : all_tags,
                                'statuses' : all_statuses,
                                'ordering' : order_by },
                              context_instance=RequestContext(request))


@login_required
def remove(request, taskid):
    task = get_object_or_404(Fptask, pk=taskid)
    if request.method == 'GET':
        return render_to_response('task/remove.html',
                                  { 'task': task },
                                  context_instance=RequestContext(request))
    else:
        task.delete()
        request.user.message_set.create(message="Task %s deleted" % taskid)
        return redirect("fp:list-tasks")
