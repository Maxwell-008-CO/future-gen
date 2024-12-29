from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('registration/',views.registration,name='registration'),
    path('login/',views.login,name='login'),
    path('chat_room/',views.chat_room,name='chat_room'),
    path('home/',views.home,name='home'),
    path('profile_view/',views.profile_view,name='profile_view'),
    path('profile_edit_login/',views.profile_edit_login,name='profile_edit_login'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('bio_view/',views.bio_view,name='bio_view'),
    path('friends/',views.friends_page,name='friends_page'),
    path('search/',views.search_friends,name='search_friends'),
    path('send_requests<int:user_id>/',views.send_friend_request,name='send_friend_request'),
    path('handle_request/<int:request_id>/<str:action>/',views.handle_request,name='handle_request'),
    path('chat_list/',views.chat_list,name='chat_list'),
    path('chat_room/<int:user_id>/',views.chat_room,name='chat_room'),
    path('groups/',views.group_list,name='group_list'),
    path('create_group/',views.create_group,name='create_group'),
    path('groups/<int:group_id>/manage/',views.manage_group,name='manage_group'),
    path('groups/<int:group_id>/chat/',views.group_chat,name='group_chat'),
    path('post_list/',views.post_list,name='post_list'),
    path('post_create/',views.post_create,name='post_create'),
    path('post/<int:pk>/edit/',views.post_edit,name='post_edit'),
    path('post/<int:pk>/delete/',views.post_delete,name='post_delete'),
    path('post_page/',views.post_page,name='post_page'),
    path('video_view/',views.video_view,name='video_view'),
    path('post_video/',views.post_video,name='post_video'),
    path('video/<int:pk>/delete/',views.video_delete,name='video_delete'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)