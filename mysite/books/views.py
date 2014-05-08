from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from books.models import Book
import datetime

# Create your views here.
def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body> It is now %s. </body></html>" % now
	return HttpResponse(html)

def index(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
	#return HttpResponse("<table>%s</table>" % '\n'.join(html))
	return HttpResponse("Welcome to page %s" % request.META['HTTP_USER_AGENT'])

#def search_form(request):
#	return render_to_response('books/search_form.html')

def search(request):
	error = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
		else:
			books = Book.objects.filter(title__icontains=q)
			return render_to_response('books/search_results.html',
				{'books': books, 'query': q})
	return render_to_response('books/search_form.html', {'error': error})