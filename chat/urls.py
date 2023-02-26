from django.contrib.auth.views import logout
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
    path('logout', logout, {'next_page': 'index'}, name='logout'),
    path('register', views.register_view, name='register'),
    path('group', views.gchat_view, name='groups'),
    path('group/<int:sender>/<int:room>', views.gmessage_view, name='group'),
    path('api/gmessages/<int:sender>/<int:room>', views.gmessage_list, name='gmessage-detail'),
    path('api/gmessages', views.gmessage_list, name='gmessage-list'),
    path('api/rooms/<int:pk>', views.room_list, name='room-detail'),
    path('api/rooms/', views.room_list, name='room-list'),
]