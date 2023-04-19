from django.urls import path
from .views import TikTokDownloadView
urlpatterns = [
    path('', TikTokDownloadView.as_view()),
]