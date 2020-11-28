from .forms import UserRegisterPage, ProfilePageForm, UserUpdateForm, PostCreationForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import login, authenticate, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from allauth import account
from .models import Post, ReadingList
# module needed in editorjs
# Create your views here.


def indexPage(request):
    context = {}
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context['page_obj'] = queryset

    return render(request, 'core/index.html', context)


def searchPost(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['q']
    blog_posts = get_blog_queryset(query)
    print('SEARCH RESULT', blog_posts)
    print('SEARCH QUERY', query)
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

    queryset = [post for post in posts]

    return list(set(queryset))


def postDetail(request, slug):
    post = Post.objects.get(slug=slug)
    try:
        reading_obj = ReadingList.objects.get(post=post)
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
    u = User.objects.get(username=user)
    post_count = u.post_set.all().count()
    comment_count = u.comment_user.all().count()

    context = {
        'user': u,
        'post_count': post_count,
        'comment_count': comment_count,
    }

    return render(request, 'core/profile.html', context)


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

        data = {
            'isBookMarked': is_True
        }

        return JsonResponse(data, safe=True)


def addPost(request):
    form = PostCreationForm()
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
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
