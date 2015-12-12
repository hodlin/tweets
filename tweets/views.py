from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


class Index(View):
	def get(self, request):
		params = {}
		params["name"] = "Django"
		return render(request, 'base.html', params)

	def post(self, request):
		return HttpResponse("I'm called from post Request")
