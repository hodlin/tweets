from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from user_profile.models import User
from .models import Tweet, HashTag
from .forms import TweetForm, SearchForm
from django.template.loader import render_to_string
from django.template import Context
import json


class Index(View):
    """ Main page view """

    def get(self, request):
        params = dict()
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
        form = TweetForm(initial={'country': 'Global'})
        params['tweets'] = tweets
        params['user'] = user
        params['form'] = form
        return render(request, 'profile.html', params)

class PostTweet(View):
    """ Tweet Post form available on page /user/<username> URL """

    def post(self, request, username):
        form = TweetForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweet(text=form.cleaned_data['text'], user=user, country=form.cleaned_data['country'])
            tweet.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word[0] == "#":
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
        return HttpResponseRedirect('/user/' + username)


class HashTagCloud(View):
    """
    Hash Tag page reachable from /hashtag/<hashtag> URL
    """

    def get(self, request, hashtag):
        params = {}
        hashtag = HashTag.objects.get(name=hashtag)
        params['tweets'] = hashtag.tweet
        return render(request, 'hashtag.html', params)


class Search(View):
    """Search a hashTag with auto complete feature"""
    def get(self, request):
        form = SearchForm()
        params = dict()
        params["search"] = form
        return render(request, 'search.html', params)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query)
            context = Context({"query": query, "tweets": tweets})
            return_str = render_to_string('partials/_tweet_search.html', context=context)
            return HttpResponse(json.dumps(return_str), content_type="application/json")
        else:
            HttpResponseRedirect("/search")
