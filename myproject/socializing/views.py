from django.shortcuts import redirect,render,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import auth,User
from .models import Message,UserProfile,FriendRequest,Friendship,Group,GroupMessage,Post,VideoPost
from .forms import ProfileForm,PostForm,VideoForm
# Create your views here.
def welcome(request):
    return render(request,'socializing/welcome.html')

def registration(request):
    print("registration page called")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username Taken')
                return redirect('registration')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,
                username=username,email=email,password=password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'passwords did not match')
            return redirect('registration')
        
    else:
        return render(request,'socializing/registration.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else :
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'socializing/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('welcome')

def home(request):
    print("home page called")
    return render(request,'socializing/homepage.html')

def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request,'socializing/profile.html',{'profile':profile})

def profile_edit_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('profile_edit')
        else :
            messages.info(request,'Ensure you are putting your account password')
            return redirect('profile_edit_login')
    return render(request,'socializing/profile_password.html')

def profile_edit(request):
    profile, created  = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = ProfileForm(request.POST,request.FILES,instance=profile)
        
        if user_form.is_valid():
            user_form.save()
            return redirect('profile_view')
    else:
        user_form = ProfileForm(instance=profile)
    return render(request,'socializing/profile_edit.html', {'user_form':user_form})

def bio_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request,'socializing/bio.html',{'profile':profile})

def friends_page(request):
    user = request.user
    friends = user.friendships.Friends.all()if hasattr(user,'friendships')else[]
    friend_requests = FriendRequest.objects.filter(receiver=user,accepted=None)
    return render(request,'socializing/friends.html',
                {'friends':friends,'friend_requests':friend_requests})

def search_friends(request):
    query = request.GET.get('q','')
    results = User.objects.filter(username=query).exclude(username=request.user.username)
    return render(request,'socializing/search.html',{'results':results,'query':query})

def send_friend_request(request,user_id):
    receiver = get_object_or_404(User,id=user_id)
    FriendRequest.objects.get_or_create(sender=request.user,receiver=receiver)
    return redirect('friends_page')

def handle_request(request,request_id,action):
    friend_request = get_object_or_404(FriendRequest,id=request_id)
    if action == 'accept':
        friend_request.accepted = True
        friend_request.save()
        sender_friendship, _ =Friendship.objects.get_or_create(user=friend_request.sender)
        receiver_friendship, _ =Friendship.objects.get_or_create(user=friend_request.receiver)
        sender_friendship.Friends.add(friend_request.receiver)
        receiver_friendship.Friends.add(friend_request.sender)
    elif action == 'decline':
        friend_request.accepted = False
    return redirect('friends_page')

def chat_list(request):
    user = request.user
    users = user.friendships.Friends.all()if hasattr(user,'friendships')else[]
    return render(request,'socializing/chat_list.html',{'users':users})

def chat_room(request,user_id):
    other_user = get_object_or_404(User,id=user_id)
    messages = Message.objects.filter(sender=request.user,
                receiver=other_user)|Message.objects.filter(sender=other_user,receiver=request.user).order_by('timestamp')
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Message.objects.create(sender=request.user,receiver=other_user,text=text)
            return redirect('chat_room',user_id=user_id)
    return render(request,'socializing/chat_room.html',{'messages':messages,'other_user':other_user})

def group_list(request):
    groups = request.user.Groups.all()
    return render(request,'socializing/group_list.html',{'groups':groups})

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('name')
        if group_name:
            group = Group.objects.create(name=group_name,admin=request.user)
            group.members.add(request.user)
            return redirect('group_list')
    return render(request,'socializing/create_group.html')

def  manage_group(request,group_id):
    group = get_object_or_404(Group,id=group_id)
    if request.user != group.admin:
        return redirect('group_list')
    if request.method == 'POST':
        if 'add_member' in request.POST:
            username = request.POST.get('username')
            try:
                user = User.objects.get(username=username)
                group.members.add(user)
            except User.DoesNotExist:
                pass
        elif 'remove_member' in request.POST:
            user_id = request.POST.get('user_id')
            user = User.objects.filter(id=user_id).first()
            if user and user != group.admin:
                group.members.remove(user)
    members = group.members.all()
    return render(request,'socializing/manage_group.html',{'group':group,'members':members})

def group_chat(request,group_id):
    group = get_object_or_404(Group,id=group_id)
    if request.user not in group.members.all():
        return redirect('group_list')
    messages = group.messages.order_by('timestamp')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            GroupMessage.objects.create(group=group,sender=request.user,text=text)
            return redirect('group_chat',group_id=group_id)
    return render(request,'socializing/group_chat.html',{'group':group,'messages':messages})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request,'socializing/post_list.html',{'posts':posts})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request,'socializing/post_form.html',{'form':form})

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if post.author != request.user:
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request,'socializing/post_form.html',{'form':form})

def post_delete(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('post_list')
    
def video_view(request):
    videos = VideoPost.objects.filter(user=request.user)
    return render(request,'socializing/videos.html',{'videos':videos})

def post_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('video_view')
    else:
        form = VideoForm()
    return render(request,'socializing/video_post.html',{'form':form})

def post_page(request):
    return render(request,'socializing/post_page.html')

def video_delete(request,pk):
    video = get_object_or_404(VideoPost,pk=pk)
    if video.user == request.user:
        video.delete()
        return redirect('video_view')