from django.shortcuts import render, redirect
import sys
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404


def index(request):
    ''' to remove duplicated topic cousing troubles
    duplicate_text = 'dance'
    Topic.objects.filter(text=duplicate_text).delete()
    '''
    return render(request, 'logs/index.html')

@login_required
def topics(request):
    '''show all topics'''
    topics = Topic.objects.order_by('date_added') # add this to private .filter(owner=request.user)
    context = {'topics':topics}
    return render(request, 'logs/topics.html', context)

@login_required
def topic(request, topic_id):
    ''' show a single topic and all entries'''
    topic = Topic.objects.get(id=topic_id)
   # check_topic_owner(request,topic)   # uncomment for private

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'logs/topic.html', context)

@login_required
def new_topic(request):
    ''' add new topic '''
    if request.method != 'POST':
        # no data submited
        form = TopicForm()
    else:
        # POST data submited
        form = TopicForm(data=request.POST)     
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user  # trying to merge all topics
            new_topic.save()
            form.save()
            return redirect('logs:topics')    
        
    # display a blank or invalid form
    context = {'form':form}
    return render(request, 'logs/new_topic.html', context)   

@login_required
def new_entry(request, topic_id):
    ''' add new entry '''
    topic = Topic.objects.get(id=topic_id)
  #  check_topic_owner(request,topic)   # uncomment for private

    if request.method != 'POST':
        # no data submited, create empty form
        form = EntryForm()
    else:
        # POST data submited
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('logs:topic',topic_id=topic_id)
    # display a blank invalid form
    context = {'topic':topic,'form':form}
    return render(request, 'logs/new_entry.html',context)        

@login_required
def edit_entry(request,entry_id):
    ''' edit an entry '''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    owner = entry.owner
    #check_topic_owner(request, topic)
    # check for entry owner and if not return to topic page....
    if entry.owner != request.user:
       # raise Http404
        return redirect('logs:topic',topic_id = topic.id) 
    
    if request.method != 'POST':
        # initial request pre-fill form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submited, proces data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic',topic_id = topic.id)
        
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request, 'logs/edit_entry.html',context)         \
    
def check_topic_owner(request, topic):
    # make sure the topic belogs to the current user
    if topic.owner != request.user:
        raise Http404    