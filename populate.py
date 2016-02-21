import os


def add_cat(name):
	c = Category.objects.get_or_create(name=name)[0]
	return c

def add_page(cat,title,url,views=0):
	p = Page.objects.get_or_create(category=cat,
			title=title,url=url,views= views)[0]
	return p




def populate():
	edu_cat = add_cat("Educational Sites")

	add_page(cat=edu_cat,
		title= "Tedx",
		url='www.tedx.org')

	add_page(cat=edu_cat,
		title= "Quora",
		url='www.quora.com')

	add_page(cat=edu_cat,
		title= "Khan Academy",
		url='www.khanacademy.org')

	add_page(cat=edu_cat,
		title= "MIT OCW",
		url='ocw.mit.edu')

	ent_cat = add_cat("Entertainment Cateegories")

	add_page(cat=ent_cat,
		title= "9gag",
		url='www.9gag.com')

	add_page(cat=ent_cat,
		title= "youtube",
		url='www.youtube.com')

	add_page(cat=ent_cat,
		title= "Twitter",
		url='www.twitter.com')

	add_page(cat=ent_cat,
		title= "kickass",
		url='www.kat.cr')

	for c in Category.objects.all():
		for p in Page.objects.filter(category = c):
			print "-{0} - {1}".format(str(c), str(p))


if __name__ == '__main__':
	#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rango.settings')
	# Raising APPRegistery not Ready error 

	from tango.models import Category, Page
	populate()
