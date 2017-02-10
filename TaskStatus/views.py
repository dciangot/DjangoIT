from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import NameForm
from RESTInterface import getFileList,getDoc
import json
from operator import itemgetter

TRANSFERDB_STATES = {0: "NEW",
                     1: "ACQUIRED",
                     2: "FAILED",
                     3: "DONE",
                     4: "RETRY",
                     5: "SUBMITTED",
                     6: "KILL",
                     7: "KILLED"}

def sortFields(listOf, field):
    """
    """
    if field and '-' not in field:
        listOf = sorted(listOf, key=itemgetter(field))
    elif '-' in field:
        listOf = sorted(listOf, key=itemgetter(field.replace('-','')), reverse=True)
    return listOf


# Create your views here.
def index(request):
    """

    """

    taskname = ''
    if request.method == 'POST':
        pass
    """
        form = IDForm(request.POST)

        if form.is_valid():
            docId = request.POST.get('docId', '')
            return render(request, 'TaskStatus/doc.html', {'form': form, 'docId': docId})
        else:
            return render(request, 'TaskStatus/index.html', {'form': form})
    """
    if request.method == 'GET':
        taskname = request.GET.get('task_name', '')
        sort = request.GET.get('order_by', '')

        if taskname: 
            form = NameForm(request.GET)
            if not form.is_valid():
                return render(request, 'TaskStatus/index.html', {'form': form})
            
            file_transfer_list = json.loads(getFileList(taskname))            

            listOf = list()
            for i in file_transfer_list['result']:
                dicto = {}
                for it, col in enumerate(file_transfer_list['desc']['columns']):
                    if col == 'tm_transfer_state':
                        dicto[col] = TRANSFERDB_STATES[i[it]]
                    else:
                        dicto[col] = i[it]

                dicto['duration'] = (dicto['tm_last_update'] - dicto['tm_start_time'])/60
                listOf.append(dicto)

            listOf = sortFields(listOf, sort)

            return render(request, 'TaskStatus/index.html', {'form': form, 'file_list': listOf})

        else:
            form = NameForm()
            return render(request, 'TaskStatus/index.html', {'form': form })


def document(request, doc_id):
    """
    """
    document = json.loads(getDoc(doc_id))            
    
    listOf = list()
    for i in document['result']:
        dicto = {}
        for it, col in enumerate(document['desc']['columns']):
            dicto[col] = i[it]

        listOf.append(dicto)
    return render(request, 'TaskStatus/document.html', {'doc': listOf })
