from django.urls import path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentDetail, CommentList, PostViewSet


app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
   path('api-token-auth/', views.obtain_auth_token),
   path('posts/<int:post>/comments/', CommentList.as_view()),
   path('posts/<int:post>/comments/<int:pk>/', CommentDetail.as_view()),
]

urlpatterns += router.urls
