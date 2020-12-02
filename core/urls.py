from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.indexPage, name='index'),
    path('post/<str:slug>/', views.postDetail, name='post-detail'),
    # path('register/', views.registerPage, name='register'),
    # path('login/', views.loginPage, name='login'),
    path('accounts/confirm/logout/', views.logoutConfirm, name='account_confirm'),
    path('accounts/logout/', views.logoutPage, name='account_logout'),
    path('profile/<str:user>/', views.profilePage, name='profile'),
    path('settings/', views.profileEditPage, name='profile-edit'),
    path('add-post/', views.addPost, name='add-post'),
    path('edit-post/<str:slug>/', views.editPost, name='edit-post'),
    path('delete-post/<str:slug>/', views.deletePost, name='delete-post'),
    path('like/<str:slug>/', views.likePost, name='like-post'),
    path('readinglist/', views.readingListPost, name='reading-list'),
    path('tagged/<str:slug>/', views.tagged, name='tagged'),
    path('readingList/<str:slug>/', views.readingListAdd, name='reading-add'),
    path('search/', views.searchPost, name='post-search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('following/<str:user>/', views.following, name='following'), path(
        'followers/<str:user>/', views.followers, name='followers'),
    # since we are not using any form to upload those images we cannot set csrf token thus we need to csrf_exempt them here and we are using requires csrf token property in views
    path('fileUPload/', csrf_exempt(views.upload_file_view)),
    path('imageUPload/', csrf_exempt(views.upload_image_view)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
