from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='static/socializing/images/profile_pictures',
        default='static/socializing/images/contact-pic.webp',
        blank=True
        )
    bio = models.TextField(blank=True,null=True)
    def __str__(self):
        return f'{self.user.username} profile'

class FriendRequest(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='send_requests')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_requests')
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(null=True)
    def __str__(self):
        return f"{self.sender.username}{self.receiver.username}"
    
class Friendship(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='friendships')
    Friends =models.ManyToManyField(User,blank=True)
    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender =models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")
    receiver =models.ForeignKey(User,on_delete=models.CASCADE,related_name="received_messages")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.text[:50]}"
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name="admin_groups")
    members = models.ManyToManyField(User,related_name="Groups",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(User,on_delete=models.CASCADE,)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message in {self.group.name} by {self.sender.username}"
    
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class VideoPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title