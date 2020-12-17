from .forms import UserRegisterPage, ProfilePageForm, UserUpdateForm, PostCreationForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import login, authenticate, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from allauth import account
from .decorators import unauthenticated_user
from .models import Post, ReadingList, Profile
from taggit.models import Tag
import json
# module needed in editorjs
# Create your views here.


def get_tag_list():
    return Post.tags.most_common()[:4]


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'core/tagged_post.html', context)


def following(request, user):
    curr_user = User.objects.get(username=user)
    profile = Profile.objects.get(user=curr_user)
    data = serializers.serialize(
        'json', profile.following.all(), fields=('username'))

    load_json = json.loads(data)
    additional_fields = []
    for field in profile.following.all():
        additional_fields.append(field.profile_img.profile.url)
    i = 0
    for f in load_json:
        load_json[i]['additional fields'] = additional_fields[i]
        i += 1

    # print('DATTAAA', data)
    context = {
        'following': load_json
    }
    return JsonResponse(context, safe=False)


def followers(request, user):
    curr_user = User.objects.get(username=user)
    profile = Profile.objects.get(user=curr_user)
    data = serializers.serialize(
        'json', profile.follower.all(), fields=('username'))

    load_json = json.loads(data)
    additional_fields = []
    for field in profile.follower.all():
        additional_fields.append(field.profile_img.profile.url)
    i = 0
    for f in load_json:
        load_json[i]['additional fields'] = additional_fields[i]
        i += 1

    # print('DATTAAA', data)
    context = {
        'followers': load_json
    }
    return JsonResponse(context, safe=False)


def socialStat(curr_user, fields, obj):
    profile = Profile.objects.get(user=curr_user)
    if obj == 'Followers':
        data = serializers.serialize(
            'json', profile.follower.all(), fields=fields)
        load_json = json.loads(data)
        additional_fields = []

        for field in profile.follower.all():
            if field in profile.following.all():
                additional_fields.append((field.profile_img.profile.url, True))
            else:
                # is_following = {'isFollwing': False}
                # additional_fields.append(is_following)
                additional_fields.append(
                    (field.profile_img.profile.url, False))

        i = 0
        for f in load_json:
            load_json[i]['additional fields'] = additional_fields[i]
            i += 1
        print(load_json)
    else:
        data = serializers.serialize(
            'json', profile.following.all(), fields=fields)
        load_json = json.loads(data)
        additional_fields = []

        for field in profile.following.all():
            additional_fields.append(field.profile_img.profile.url)
        i = 0
        for f in load_json:
            load_json[i]['additional fields'] = additional_fields[i]
            i += 1

    return load_json


def dashboardData(request, category):
    curr_user = get_object_or_404(User, username=request.user)
    if category == 'Post':
        data = serializers.serialize(
            'json', curr_user.post_set.filter(draft=False), fields=('title', 'draft', 'slug'))
    elif category == 'Draft':
        data = serializers.serialize('json', curr_user.post_set.filter(
            draft=True), fields=('title', 'draft', 'slug'))
    elif category == 'Following':
        fields = ('username')
        data = socialStat(curr_user, fields, category)
        # data = curr_user.profile_img.following.all()
    elif category == 'Followers':
        fields = ('username')
        data = socialStat(curr_user, fields, category)
        # data = curr_user.profile_img.follower.all()
    elif category == 'Comment':
        slugs = [comment.post.slug for comment in curr_user.comment_user.all()]
        # date = [d.created.time for d in curr_user.comment_user.all()]
        
        data = serializers.serialize('json', curr_user.comment_user.all(), fields=('post', 'created','comment',), use_natural_foreign_keys=True)

    context = {
        'data': data
    }
    return JsonResponse(context, safe=False)


def followAdd(request, user):

    curr_user = get_object_or_404(User, username=request.user)
    target_user = get_object_or_404(User, username=user)

    if target_user in curr_user.profile_img.following.all():
        curr_user.profile_img.following.remove(target_user)
        target_user.profile_img.follower.remove(curr_user)
        data = 'Follow'
    else:
        curr_user.profile_img.following.add(target_user)
        target_user.profile_img.follower.add(curr_user)
        data = 'Following'

    return JsonResponse({'data': data}, safe=False)


def indexPage(request):
    context = {}
    if request.user.is_authenticated:
        curr_user = User.objects.get(username=request.user)
        try:
            reading_obj = ReadingList.objects.get(user=curr_user)
            context['reading_obj'] = reading_obj
        except:
            reading_obj = ReadingList.objects.create(user=curr_user)
            reading_obj.save()

    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context['page_obj'] = queryset
    context['common_tags'] = get_tag_list

    return render(request, 'core/index.html', context)


def searchPost(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['q']
    blog_posts = get_blog_queryset(query)
    print('data to be serve', blog_posts)
    context['blog_posts'] = blog_posts
    return render(request, 'core/search_result.html', context)


def get_blog_queryset(query=None):  # this will be used in search
    queries = query.split(' ')
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q),
            Q(body__icontains=q),
            Q(snippet__icontains=q),
        ).distinct()
    print('found posts', posts)
    queryset = [post for post in posts]
    print('queryset to be pass', queryset)

    return list(set(queryset))


def postDetail(request, slug):
    curr_user = User.objects.get(username=request.user)
    post = Post.objects.get(slug=slug)
    try:
        reading_obj = ReadingList.objects.get(user=curr_user)
    except:
        reading_obj = False
    context = {
        'reading_obj': reading_obj,
        'post': post
    }

    return render(request, 'core/post_detail.html', context)


# def registerPage(request):
#     forms = UserRegisterPage()

#     if request.method == 'POST':
#         forms = UserRegisterPage(request.POST)
#         if forms.is_valid():
#             forms.save()
#             return redirect('login')

#     context = {
#         'forms': forms
#     }
#     return render(request, 'core/register.html', context)


# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 messages.info(request, 'You entered invalid credentials')
#     return render(request, 'core/login.html')


def logoutConfirm(request):
    return render(request, 'account/logout.html')


def logoutPage(request):
    logout(request)
    return redirect('account_login')


def profilePage(request, user):
    curr_user = get_object_or_404(User, username=request.user)
    u = get_object_or_404(User, username=user)
    post_count = u.post_set.all().count()
    comment_count = u.comment_user.all().count()
    following_count = u.profile_img.following.all().count()
    follower_count = u.profile_img.follower.all().count()

    context = {
        'user': u,
        'post_count': post_count,
        'comment_count': comment_count,
        'following_count': following_count,
        'followers_count': follower_count,
    }

    if u in curr_user.profile_img.following.all():
        context['is_true'] = True

    return render(request, 'core/profile.html', context)


@unauthenticated_user
def profileEditPage(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilePageForm(
            request.POST, request.FILES, instance=request.user.profile_img)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has successfully updated')
            return redirect('profile', request.user)
    else:

        # for account in request.user.socialaccount_set.all():
        #     avatar = account.get_avatar_url()
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilePageForm(instance=request.user.profile_img)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
    return render(request, 'core/profile_edit.html', context)


def likePost(request, slug):
    user = request.user
    if request.method == 'POST':

        # print('CHECKING SLUG', post_slug)
        post_obj = Post.objects.get(slug=slug)
        profile = User.objects.get(username=user)

        if profile not in post_obj.likes.all():
            post_obj.likes.add(profile)
            like = True
        else:
            post_obj.likes.remove(profile)
            like = False

        data = {
            'likes': post_obj.likes.all().count(),
            'is_like': like
        }

        return JsonResponse(data, safe=False)


def readingListPost(request):
    curr_user = User.objects.get(username=request.user)
    try:
        read_obj = ReadingList.objects.get(user=curr_user)
    except:
        read_obj = False
    context = {
        'read_obj': read_obj
    }

    return render(request, 'core/reading_list.html', context)


def readingListAdd(request, slug):
    user = request.user

    if request.method == 'POST':
        post_obj = Post.objects.get(slug=slug)
        curr_user = User.objects.get(username=user)
        try:
            read_obj = ReadingList.objects.get(user=curr_user)
        except:
            reading_create = ReadingList.objects.create(user=curr_user)
            reading_create.post.add(post_obj)
            reading_create.save()
            return JsonResponse({}, safe=False)

        if post_obj in read_obj.post.all():
            read_obj.post.remove(post_obj)
            is_True = False
        else:
            read_obj.post.add(post_obj)
            is_True = True

        print('checkk', is_True)
        data = {
            'post': post_obj.title,
            'isBookMarked': is_True
        }

        return JsonResponse(data, safe=True)


def dashboard(request):
    curr_user = User.objects.get(username=request.user)
    post = curr_user.post_set.filter(draft=False)
    draft_count = curr_user.post_set.filter(draft=True).count()
    following_count = curr_user.profile_img.following.all().count()
    followers_count = curr_user.profile_img.follower.all().count()
    context = {
        'posts': post,
        'draft_count': draft_count,
        'following_count': following_count,
        'followers_count': followers_count,
    }

    return render(request, 'core/dashboard.html', context)


def addPost(request):
    form = PostCreationForm()
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            form.save_m2m()
            return redirect('index')
    context = {
        'forms': form
    }
    return render(request, 'core/add_post.html', context)


def editPost(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')

    form = PostCreationForm(instance=post)
    context = {
        'forms': form
    }

    return render(request, 'core/add_post.html', context)


def deletePost(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return redirect('index')


@requires_csrf_token
def upload_image_view(request):  # editorjs for uploading image
    f = request.FILES['image']  # getting the image from editorjs
    fs = FileSystemStorage()
    # converting f to str and split it in two first part is name and the second part is the extension and we only need the name of the file
    filename = str(f).split('.')[0]
    # we passed the file to systemstorage and save it
    file = fs.save(filename, f)
    fileurl = fs.url(file)  # create file url we already created
    return JsonResponse({'success': 1, 'file': {'url': fileurl}})


# @requires_csrf_token
# def upload_file_view(request):  # editorjs for uploading file
#     f = request.FILES['file']
#     fs = FileSystemStorage()
#     filename, ext = str(f).split('.')
#     file = fs.save(filename, f)
#     fileurl = fs.url(file)
#     return JsonResponse({
#         'success': 1,
#         'file': {
#             'url': fileurl, 'size': fs.size(filename), "name": str(f), "extension": ext
#         }
#     })


@requires_csrf_token
def upload_file_view(request):
    f = request.FILES['file']
    fs = FileSystemStorage()
    filename, ext = str(f).split('.')
    file = fs.save(str(f), f)
    fileurl = fs.url(file)
    return JsonResponse({'success': 1,
                         'file':
                         {'url': fileurl,
                          "size": fs.size(filename),
                             "name": str(f),
                             "extension": ext}
                         })
