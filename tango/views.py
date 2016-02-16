from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


# Create your views here.
def index(request):
	#return HttpResponse("Tango says hello world!")
	#Request the context of the request.
	# The context contains information such as the clients 
	#machine details.
	context = RequestContext(request)
	#Construct a dictionary to pass to the template engine as its context
	context_dict = {"bold_message": "I am Rango"}

	return render_to_response("tango/index.html", context_dict, context)


def about(request):
	#return HttpResponse("This is me! I will update later.")

	context = RequestContext(request)
	context_dict = {"about_rango": " Horray This is rango"}

	return render_to_response("tango/about.html", context_dict, context)

