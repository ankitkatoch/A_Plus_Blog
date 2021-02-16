from django.urls import path, include
from .views import (BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView,
                    BlogDeleteView, BlogSearchView, TagIndexView, BlogListHomeView, share_with_friends)

urlpatterns = [
    path('', BlogListHomeView.as_view(), name='home'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('list/', BlogListView.as_view(), name='blog_list'),
    path('detail/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('update/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<slug:slug>', TagIndexView.as_view(), name='tagged'),
    path('search/', BlogSearchView.as_view(), name='blog_search'),
    path('share/', share_with_friends, name='share_with_friends'),
]
