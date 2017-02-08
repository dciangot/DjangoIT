import pycurl
import cStringIO as StringIO
import urllib
import json


class ResponseHeader(object):
    """ResponseHeader parses HTTP response header"""
    def __init__(self, response):
        super(ResponseHeader, self).__init__()
        self.header = {}
        self.reason = ''
        self.fromcache = False
        self.parse(response)

    def parse(self, response):
        """Parse response header and assign class member data"""
        for row in response.split('\r'):
            row = row.replace('\n', '')
            if  not row:
                continue
            if  row.find('HTTP') != -1 and \
                row.find('100') == -1: #HTTP/1.1 100 found: real header is later
                res = row.replace('HTTP/1.1', '')
                res = res.replace('HTTP/1.0', '')
                res = res.strip()
                status, reason = res.split(' ', 1)
                self.status = int(status)
                self.reason = reason
                continue
            try:
                key, val = row.split(':', 1)
                self.header[key.strip()] = val.strip()
            except:
                pass


def parse_body(data, decode=False):
    """
    Parse body part of URL request (by default use json).
    This method can be overwritten.
    """
    if  decode:
        try:
            res = json.loads(data)
        except ValueError as exc:
            msg = 'Unable to load JSON data, %s, data type=%s, pass as is' \
                    % (str(exc), type(data))
            logging.warning(msg)
            return data
        return res
    else:
        return data

def parse_header(header):
    """
    Parse response header.
    This method can be overwritten.
    """
    return ResponseHeader(header)



def getFileList(taskname):
    """
    get list of file to be tranferred
    Query:
    """
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.TIMEOUT, 300)
        c.setopt(pycurl.CONNECTTIMEOUT, 300)
        #c.setopt(pycurl.GET, 1)

        fileDoc = {}
        fileDoc['taskname'] = taskname
        fileDoc['username'] = taskname.split(':')[1].split('_')[0]
        fileDoc['subresource'] = 'getTransferStatus'

        c.setopt(pycurl.URL, 'https://asotest3.cern.ch/crabserver/dev/fileusertransfers' + '?' + urllib.urlencode(fileDoc) )

        url = 'https://asotest3.cern.ch/crabserver/dev/fileusertransfers' + '?' + urllib.urlencode(fileDoc)

        #c.setopt(pycurl.POSTFIELDS, urllib.urlencode(fileDoc))
        bbuf = StringIO.StringIO()
        hbuf = StringIO.StringIO()

        proxy = '/home/dciangot/proxy' 

        c.setopt(pycurl.WRITEFUNCTION, bbuf.write)
        c.setopt(pycurl.HEADERFUNCTION, hbuf.write)
        c.setopt(pycurl.CAPATH, '/etc/grid-security/certificates/')
        c.setopt(pycurl.SSL_VERIFYPEER, True)
        c.setopt(pycurl.SSLKEY, proxy)
        c.setopt(pycurl.SSLCERT, proxy)
        c.setopt(pycurl.VERBOSE, 1)

        c.perform()

        header = parse_header(hbuf.getvalue())
        if  header.status < 300:
            data = parse_body(bbuf.getvalue())
        else:
            data = bbuf.getvalue()
            msg = 'url=%s, code=%s, reason=%s, headers=%s' \
                    % (url, header.status, header.reason, header.header)
            bbuf.flush()
            hbuf.flush()
            return {msg}

        bbuf.flush()
        hbuf.flush()
      
        print data

    except Exception as ex:
        print ('Error during connection to cmsweb: ' + str(ex))
        return {}

    return data

