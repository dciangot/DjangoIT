from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import NameForm

# Create your views here.
def index(request):
    

    taskname = ''

    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            taskname = request.POST.get('task_name', '')
            return render(request, 'TaskStatus/index.html', {'form': form, 'taskname': taskname})
        else:
            return render(request, 'TaskStatus/index.html', {'form': form})

    elif request.method == 'GET':
        taskname = request.GET.get('task_name', '')

        if taskname: 
            form = NameForm(request.GET)
            if not form.is_valid():
                return render(request, 'TaskStatus/index.html', {'form': form})
            
            return render(request, 'TaskStatus/index.html', {'form': form, 'taskname': taskname})

        else:
            form = NameForm()
            return render(request, 'TaskStatus/index.html', {'form': form})



