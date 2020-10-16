from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Court, Decision
from django.template import loader
from .forms import NameForm


def home(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            query_data = form.cleaned_data
            decisions = Decision.objects.all()
            # court
            if query_data['court'] is not None:
                decisions = decisions.filter(court=query_data['court'])
            # type
            if query_data['file_type'] is not "":
                decisions = decisions.filter(file_type=query_data['file_type'])
            # dates, pronounced, created, published
            if query_data['date_created_from'] is not None:
                decisions = decisions.filter(date_created__gte=query_data['date_created_from'])
            if query_data['date_published_from'] is not None:
                decisions = decisions.filter(date_published__gte=query_data['date_published_from'])
            if query_data['date_pron_from'] is not None:
                decisions = decisions.filter(date_pron__gte=query_data['date_pron_from'])
            if query_data['date_created_to'] is not None:
                decisions = decisions.filter(date_created__lte=query_data['date_created_to'])
            if query_data['date_published_to'] is not None:
                decisions = decisions.filter(date_published__lte=query_data['date_published_to'])
            if query_data['date_pron_to'] is not None:
                decisions = decisions.filter(date_pron__lte=query_data['date_pron_to'])
            # file name
            if query_data['file_name'] is not "":
                decisions = decisions.filter(file_name__search=query_data['file_name'].strip())
            # theme
            if query_data['file_theme'] is not "":
                decisions = decisions.filter(file_theme__search=query_data['file_theme'].strip())
            # content
            if query_data['file_content'] is not "":
                decisions = decisions.filter(file__search=query_data['file_content'].strip())

            template = loader.get_template('rcdd/home.html')
            context = {
                'decisions': decisions,
                'form': form
            }
            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('rcdd/home.html')
            form = NameForm()
            context = {
                'form': form
            }
            return HttpResponse(template.render(context, request))
    else:
        decisions = Decision.objects.order_by('-id')[:20]
        template = loader.get_template('rcdd/home.html')
        form = NameForm()
        context = {
            'decisions': decisions,
            'form': form
        }
        return HttpResponse(template.render(context, request))


def decision(request):
    # return decision text for given id
    id = request.GET.get('id')
    file = Decision.objects.filter(file_number=id)[0].file
    return HttpResponse(file)
