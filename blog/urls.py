from django.urls import path
from blog import views

urlpatterns = [
    path('posts/', 
    views.PostListView.as_view(), 
    name="post_list"),

    path('about/', 
    views.AboutView.as_view(), 
    name="about"),

    path('post/<int:pk>/', 
    views.PostDetailView.as_view(), 
    name="post_detail"),

    path('createpost/', 
    views.CreatePostView.as_view(), 
    name="createpost"),

    path('post/<int:pk>/edit/', 
    views.UpdatePostView.as_view(), 
    name="editpost"),

    path('post/<int:pk>/delete/', 
    views.PostDeleteView.as_view(), 
    name="deletepost"),

    path('drafts/',
    views.PostDraftView.as_view(),
    name="drafts"),

    path('post/<int:pk>/comment',
    views.add_comment_to_post,
    name="add_comment_to_post"),

    path('comment/<int:pk>/approve/',
    views.approve_comment,
    name="approve_comment"),

    path('comment/<int:pk>/delete/',
    views.delete_comment,
    name="delete_comment"),

    path('comment/<int:pk>/publish/',
    views.publish_post,
    name="publish_post")    
]