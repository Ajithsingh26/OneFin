from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterView, MovieListView, CollectionViewSet, RequestCountView, ResetRequestCountView
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'collection', CollectionViewSet, basename='collection')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('request-count/', RequestCountView.as_view(), name='request_count'),
    path('request-count/reset/', ResetRequestCountView.as_view(), name='reset_request_count'),
    path('', include(router.urls)),
]