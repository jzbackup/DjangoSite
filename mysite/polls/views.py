from polls.models import Poll, Choice
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.core.urlresolvers import reverse
import datetime
import json

# Create your views here.
def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body> It is now %s. </body></html>" % now
	return HttpResponse(html)

def index(request):
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	#more concise way
	return render_to_response('polls/index.html',
								{'latest_poll_list': latest_poll_list})
	
	#t = loader.get_template('polls/index.html')
	#c = Context({
	#	'latest_poll_list': latest_poll_list,
	#})
	#return HttpResponse(t.render(c))
	
	#output = ', '.join([p.question for p in latest_poll_list])
	#return HttpResponse(output)
	#return HttpResponse("Hello, world. You're at the poll index.")
	
def detail(request, poll_id):
	#shortcut way
	p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('polls/detail.html', {'poll':p},
								context_instance=RequestContext(request))
	#return render_to_response('polls/detail.html', {'poll':p})
	
	#try:
	#	p = Poll.objects.get(pk=poll_id)
	#except Poll.DoesNotExist:
	#	raise Http404
	#return render_to_response('polls/detail.html', {'poll': p})
	#return HttpResponse("You're looking at poll %s." % poll_id)
	
def results(request, poll_id):
		
	if request.method == 'POST':	
		p = get_object_or_404(Poll, pk=poll_id)
		return render_to_response('polls/results.html', {'poll':p})
		#return HttpResponse("You're looking at the results of poll %s." % poll_id)
	
	#handle the json request
	if request.GET.get('format','')=='json':
		#p = get_object_or_404(Poll, pk=poll_id)
		#return render_to_response('polls/results.html', {'poll':p})

		userName=request.GET['name']
		passWord=request.GET['password']
		
		data={}
		data['name'] = userName
		data['password'] = passWord
		data['id'] = "id"
		response={}
		response['data'] = data
		all={}
		all['response']=response
		all['status']='ok'
		return HttpResponse(json.dumps(all), content_type="application/json")
		


def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render_to_response('polls/detail.html', {
			'poll': p,
			'error_message': "You didn't select a choice.",
		}, context_instance=RequestContext(request))
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls.views.results',
											args=(p.id,)))
	return HttpResponse("You're voting on poll %s." % poll_id)