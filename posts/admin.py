from django.contrib import admin
from posts.models import Tweets

class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'text', 'created_at', 'updated_at')

admin.site.register(Tweets, TweetAdmin)



# Register your models here.
