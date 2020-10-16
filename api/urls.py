from django.urls import path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet


app_name = 'posts'

router = DefaultRouter()
router.register(r'v1/posts', PostViewSet)
router.register(r'v1/posts/(?P<post>\d+)/comments', CommentViewSet)

urlpatterns = [
   path('v1/api-token-auth/', views.obtain_auth_token),
]

urlpatterns += router.urls
