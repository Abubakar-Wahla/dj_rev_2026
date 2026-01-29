from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views_cbv import ProjectDetailAPIView,ProjectListCreateAPIView,MyProjectsAPIView

urlpatterns = [
    path("", views.get_routes, name="api-routes"),
    path("projects/", ProjectListCreateAPIView.as_view(), name="api-projects"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("projects/<uuid:pk>/",ProjectDetailAPIView.as_view(),name="api-project-detail"),
    path("projects/my/", MyProjectsAPIView.as_view(), name="api-my-projects"),

]
