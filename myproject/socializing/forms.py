from django import forms
from .models import UserProfile,Post,VideoPost
from django.contrib.auth.models import User
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','bio']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ['title','description','video_file']