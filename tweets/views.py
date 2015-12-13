from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from user_profile.models import User
from tweets.models import Tweet


class Index(View):
	""" Main page view """

	def get(self, request):
		params = {}
		params["name"] = "Django"
		return render(request, 'base.html', params)

	def post(self, request):
		return HttpResponse("I'm called from post Request")


class Profile(View):
	""" User Profile page reachable from /user/<username>/ URL """

	def get(self, request, username):
		params = {}
		user = User.objects.get(username=username)
		tweets = Tweet.objects.filter(user=user)
		params['tweets'] = tweets
		params['user'] = user
		return render(request, 'profile.html', params)
