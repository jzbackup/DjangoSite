from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse

def contact(request):
	errors = []
	if request.method == 'POST':
		if not request.POST.get('subject', ''):
			errors.append('Enter a subject')
		if not request.POST.get('message', ''):
			errors.append('Enter a message.')
		if request.POST.get('email') and '@' not in request.POST['email']:
			errors.append('Enter a valid e-mail address.')
		if not errors:
			send_mail(
				request.POST['subject'],
				request.POST['message'],
				request.POST.get('email', 'noreply@example.com'),
				['zhaojinhust@gmail.com'],
			)
			#return HttpResponseRedirect('.contact.thanks/')
			return HttpResponse("ok")
	return render_to_response('contact/contact_form.html', 
		{'errors':errors},
		context_instance=RequestContext(request))

def thanks(request):
	thanks = 'thank you for your email'
	return HttpResponse("<table>%s</table>" % thanks)