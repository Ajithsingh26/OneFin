from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterView, MovieListView, CollectionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'collection', CollectionViewSet, basename='collection')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('', include(router.urls)),
]