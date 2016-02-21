from django.shortcuts import render, render_to_response
#from django.http import HttpResponse
from django.template import RequestContext
from tango.models import Category
from .models import Page, Category
from tango.forms import CategoryForm, PageForm
from tango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User




def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')



def index(request):
	#return HttpResponse("Tango says hello world!")
	#Request the context of the request.
	# The context contains information such as the clients 
	#machine details.
	context = RequestContext(request)
	#Construct a dictionary to pass to the template engine as its context
	category_list = Category.objects.order_by('-likes')
	#context_dict = {"categories": category_list}

	for category in category_list:
		category.url = category.name.replace(' ', '_')
		if category.url.endswith('/') == False:
			category.url += '/'

	context_dict = {"categories": category_list}

	return render_to_response("tango/index.html", context_dict, context)


def about(request):
	#return HttpResponse("This is me! I will update later.")

	context = RequestContext(request)
	context_dict = {"about_rango": " Horray This is rango"}

	return render_to_response("tango/about.html", context_dict, context)

"""
def cat(request):
	context = RequestContext(request)
	cats = Category.objects.all()
	context_dict = {"cats", cats}

	return render_to_response("tango/cat.html", context_dict
		,context)
"""


def category(request, category_name_url):
	context = RequestContext(request)
	#category_name = category_name_url.replace("_", ' ')
	category_name = decode_url(category_name_url)

	context_dict = {'category_name': category_name}
	context_dict['category_name_url'] = category_name_url

	try:
		category = Category.objects.get(name = category_name)
		pages = Page.objects.filter(category = category)

		context_dict["pages"] = pages
		context_dict["category"] = category

	except Category.DoesNotExist:
		pass

	return render_to_response("tango/category.html", context_dict,context)

@login_required
def add_category(request):

	context = RequestContext(request)

	if request.method == "POST":
		form  = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return index(request)

		else:
			print form.errors
	else:
		form = CategoryForm()

	return render_to_response('tango/add_category.html',
				{'form': form}, context)

@login_required
def add_page(request, category_name_url):


	context = RequestContext(request)
	category_name = decode_url(category_name_url)


	if request.method == "POST":
		form  = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)
			cat = Category.objects.get(name=category_name)
			page.category = cat
			page.views = 0
			page.save()

			return category(request, category_name_url)


		else:
			print form.errors
	else:
		form = PageForm()

	#return render_to_response('tango/add_category.html',
	#			{'form': form}, context)

	return render_to_response( 'tango/add_page.html',
							{'category_name_url': category_name_url,
							'category_name': category_name, 'form': form},
							context)


def register(request):

	context = RequestContext(request)

	registered = False
	# A boolean value for telling template that registeration
	#was successful

	if request.method == "POST":

		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			#hash the password with set_password

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user
			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form  = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'tango/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered' : registered},
		context)

		
def user_login(request):

	context = RequestContext(request)

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/tango/')
			else:
				return HttpResponse("Your acccount is disabled")

		else:
			print "Invalid login details [0], [1]".format[username, password]
			return HttpResponse("Invalid login details supplied.")

	else:

		return render_to_response('tango/login.html', {}, context)


@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/tango/')

@login_required
def profile(request):
	context = RequestContext(request)
	#cat_list = get_category_list()
	#context_dict = {'cat_list': cat_list}
	u = User.objects.get(username=request.user)
	try:
		up = UserProfile.objects.get(user=u)
	except:
		up = None

	context_dict = {'user' : u }
	context_dict['userprofile'] = up
	return render_to_response('tango/profile.html', context_dict, context)
