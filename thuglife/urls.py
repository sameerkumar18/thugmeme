from django.urls import path

from thuglife.views import thug_meme, text_meme


urlpatterns = [
    path('thug_meme/', thug_meme),
    path('text_meme/', text_meme),
]
