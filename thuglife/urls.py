from django.urls import path, include

from thuglife.views import thug_meme, text_meme, test_task


urlpatterns = [
    path('thug_meme/', thug_meme),
    path('text_meme/', text_meme),
    path('lol/', test_task)
]