from django.urls import path
from . import views

app_name = 'logs'
urlpatterns = [
    # home page
		path('', views.index, name='index'),
        # topic page
		path('topics/', views.topics, name='topics'),
        # page for each topic
		path('topics/<int:topic_id>/', views.topic, name='topic'),
        # page to add new topics
		path('new_topic/', views.new_topic, name='new_topic'),
        # new entry
		path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
        # page to edit entries
		path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
	]