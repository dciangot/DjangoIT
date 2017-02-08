from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import NameForm
import pycurl
import cStringIO as StringIO
import urllib

def getFileList(taskname):
    """
    get list of file to be tranferred
    Query:
    """
    c = pycurl.Curl()
    c.setopt(pycurl.TIMEOUT, 300)
    c.setopt(pycurl.CONNECTTIMEOUT, 300)
    c.setopt(pycurl.POST, 1)

    c.setopt('cmsweb.cern.ch/crabserver/prod/fileusertransfers', url)

	fileDoc = {}
	fileDoc['taskname'] = taskname
	fileDoc['username'] = taskname
	fileDoc['subresource'] = 'getTransferStatus'

    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(fileDoc))
    bbuf = StringIO.StringIO()
    hbuf = StringIO.StringIO()

    c.setopt(pycurl.WRITEFUNCTION, bbuf.write)
    c.setopt(pycurl.HEADERFUNCTION, hbuf.write)
    curl.setopt(pycurl.CAPATH, proxy)
    curl.setopt(pycurl.SSL_VERIFYPEER, True)
    c.setopt(pycurl.SSLKEY, proxy)
    c.setopt(pycurl.SSLCERT, proxy)

    try:
        curl.perform()
    except:
        print ('Error during connection to cmsweb')
        return {}

	header = self.parse_header(hbuf.getvalue())
	if  header.status < 300:
		if  verb == 'HEAD':
			data = ''
		else:
			data = self.parse_body(bbuf.getvalue(), decode)
	else:
		data = bbuf.getvalue()
		msg = 'url=%s, code=%s, reason=%s, headers=%s' \
				% (url, header.status, header.reason, header.header)
		bbuf.flush()
		hbuf.flush()
        return {}

	bbuf.flush()
	hbuf.flush()

    return data

# Create your views here.
def index(request):
    """

    """

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
            
            file_transfer_list = getFileList(taskname)            

            return render(request, 'TaskStatus/index.html', {'form': form, 'file_list': file_transfer_list})

        else:
            form = NameForm()
            return render(request, 'TaskStatus/index.html', {'form': form})



