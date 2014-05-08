from django.contrib import admin
from bikeends.models import User, Ride, FriendshipManager, Friendship, FriendshipRequest
# Register your models here.

admin.site.register(User)
admin.site.register(Ride)
#admin.site.register(FriendshipManager)
admin.site.register(Friendship)
admin.site.register(FriendshipRequest)