from django.urls import path
from .views import PostDetailView, post_list,post_search,AboutView,ContactView

app_name = 'exam'

urlpatterns = [

    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', post_search, name='post_search'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('category/<int:category_id>/', post_list, name='post_by_category'),

]

