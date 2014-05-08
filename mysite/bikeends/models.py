from django.db import models
import datetime

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField()
	age = models.IntegerField('Age')
	#0 is female, 1 is male
	
	#? how to use bool?
	
	sex = models.IntegerField()
	signature = models.CharField(max_length = 1000)
	#image is a url to a static file in the server
	image = models.URLField()
	join_data = models.DateTimeField('data joined')
	#should also has friends and rides, but should these be achieve by foreign keys?
	#friends-friends: many to many
	#friends = models.ForeignKey('self', null=True, blank=True, default=None)
	def __unicode__(self):
		return self.name
		
class Ride(models.Model):
	#use foreign key to relate the rides to users: 1 to many
	user = models.ForeignKey(User)
	starttime = models.DateTimeField()
	endtime = models.DateTimeField()
	#duration2 = models.IntegerField()import 
	data = models.URLField()
	def __unicode__(self):
		return self.data
		
class FriendshipManager(models.Manager):
	def friends_of(self, user, shuffle=False):
		qs = User.objects.filter(friendship__friends__user=user)
		if shuffle:
			qs = qs.order_by('?')
		return qs
		
	def are_friends(self, user1, user2):
		friendship = Friendship.objects.get(user=user1)
		return bool(friendship.friends.filter(user=user2).exists())
	
	def befriend(self, user1, user2):
		friendship = Friendship.objects.get(user=user1)
		friendship.friends.add(Friendship.objects.get(user=user2))
		FriendshipRequest.objects.filter(from_user=user1,to_user=user2).delete()
		#pass
		
	def unfriend(self, user1, user2):
		friendship = Friendship.objects.get(user=user1)
		friendship.friends.remove(Friendship.objects.get(user=user2))
		FriendshipRequest.objects.filter(from_user=user1, to_user=user2).delete()
		FriendshipRequest.objects.filter(from_user=user2, to_user=user1).delete()
		
class Friendship(models.Model):
	user = models.OneToOneField(User, related_name='friendship')
	#friends = models.ManyToManyField(User, related_name='friends+', symmetrical=True)
	friends = models.ManyToManyField('self', symmetrical=True)
	objects = FriendshipManager()
	
	"""
	class Meta:
		verbose_name = 'friendship'
		verbose_name_plural = 'friendships'
	"""
	def __unicode__(self):
		#return (u'%(user)s\'s friends') % {'user': unicode(self.user)}
		return self.friends.count()
		
	def friend_count(self):
		return self.friends.count()
		
class FriendshipRequest(models.Model):
	from_user = models.ForeignKey(User, related_name="friendshiprequests_from")
	to_user = models.ForeignKey(User, related_name="friendshiprequests_to")
	created = models.DateTimeField(default=datetime.datetime.now,editable=False)
	accepted = models.BooleanField(default=False)
	
	def __unicode__(self):
		return (u'%(from_user)s wants to be friends with %(to_user)s') %{
			'from_user': unicode(self.from_user),
			'to_user': unicode(self.to_user)
		}
	
	def accept(self):
		Friendship.objects.befriend(self.from_user, self.to_user)
		self.accepted = True
		self.save()
		
	def decline(self):
		self.delete()

	