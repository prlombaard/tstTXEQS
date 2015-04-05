__author__ = '0400428'

#Example 4-8. handle_post.py

from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from calendar import calendar
from datetime import datetime, date, time
from twisted.web.util import redirectTo
import sys
from subprocess import Popen
from os import pipe, devnull
from time import sleep

# global module variables
# TODO: Add server global variables here
server_state = ""
server_starttime = datetime.today()
server_number_of_views = 0

# TODO: Load securely from config file
server_users_and_passwords = {'user': 'user', 'admin': 'admin'}
server_debugmode = "logging off"
server_txmode_string = ['Fixed Frequency', 'Sweep Frequency', 'Hop Frequency', 'Off']
server_varheader = ['txmode', 'fixedstart', 'fixedstop', 'hopdelay', 'sweepstart', 'sweepstop']

server_logging_mode = {'Append Log': 'Logging on', 'Rewrite log': 'Logging on', 'Off': 'Logging'}


server_vars = {server_varheader[0]: server_txmode_string[0], server_varheader[1]: 1000000, server_varheader[2]: 1200000, server_varheader[3]: 200, server_varheader[4]: 1000000, server_varheader[5]: 1200000}

# piFM related variables
music_pipe_r, music_pipe_w = pipe()
fm_process = None

# TODO: Add logging like in import logging


def isRunning(processid):
    #print "isrunning:Start"
    try:
        if (processid.poll() is not None) or (processid is None):
            #print "process pid[%d] have terminated with exitcode [%d]" % (fm_process.pid, fm_process.poll())
            return False
        else:
            return True
    except TypeError as e1:
        #print "process pid[%d] have not yet terminated" % (fm_process.pid)
        #print "TypeError %s" % e1
        return True
    except AttributeError as e2:
        #print "process pid[%d] have not yet terminated" % (fm_process.pid)
        #print "AttributeError %s" % e2
        return False


def runprun_pifm():
    global fm_process

    # TODO: Only create, terminate process if transmitter parameters have changed

    # TODO: Move the platform checking out of this method, use common array name in Popen, i.e. not hardcoded string literals
    if sys.platform.startswith('win'):
        print "Platform : Windows"

        with open(devnull, "w") as dev_null:
            # Create the process in specific platform modes
            # TODO: create processes in different ways depending on Transmitter Mode
#            if server_vars[server_varheader[0]] == server_txmode_string[0]:
            # Transmit mode is set to Fixed Frequency
            # Test if fm_process is already running
            if isRunning(fm_process) == False:
                # Process not running so create new one
                pass
            else:
                # Process already created and running
                # Terminate current pifm process
                try:
                    print "Process already exists, terminating"
                    fm_process.terminate()
                except AttributeError:
                    pass
                # TODO: Check how long to wait before creating new process
                sleep(1)

            print "Creating new process"
            fm_process = Popen(["ping", "127.0.0.1", "-t"], stdin=music_pipe_r, stdout=dev_null)
            #fm_process = Popen(["ping", "127.0.0.1", "-t"], stdin=music_pipe_r)

            print "fm process PID [%d]" % (fm_process.pid)
    else:
        print "Platform : Linux"
        with open(devnull, "w") as dev_null:
            # TODO: Temporary fix if os is Windows then use pipe otherwise use the real command assuming were on rPi platform
            fm_process = Popen(["/root/pifm", "-", str(frequency), "44100", "stereo" if play_stereo else "mono"], stdin=music_pipe_r, stdout=dev_null)


class YearPage(Resource):
    # TODO: Add class comment here
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        global server_number_of_views
        server_number_of_views += 1

        return "<title>Calender for %s</title><html><body><pre>%s</pre></body></html>" % (self.year,calendar(self.year))


class AboutPage(Resource):
    # TODO: Add class comment here
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        global server_number_of_views
        server_number_of_views += 1

        return "<html><body><pre>%s</pre></body></html>" % ("About this page",)


class ConfigPage(Resource):
    # TODO: Add class comment here
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        global server_number_of_views
        server_number_of_views += 1

        return """
        <title>Config Page</title>
        <h1>Config Page</h1>
        <form method="post"

         <fieldset>
          <legend> Debug Mode</legend>
          <p><label> <input type=radio name=logging_mode required value="logging append" > Logging  on : append log </label></p>
          <p><label> <input type=radio name=logging_mode required value="logging rewrite"> Logging  on : rewrite log </label></p>
          <p><label> <input type=radio name=logging_mode required value="logging off">     Logging     : off </label></p>
         </fieldset>

         <p><button>Submit</button></p>
        </form>
        """

    def render_POST(self, request):
        print "FormPage::render_POST"

        print "Methods and Attributes of request"
        for i in request.__dict__:
            print "[%s]:[%s]" % (i, getattr(request, i))

        print "Request.args:"
        if request.args is not None:
            for k, v in request.args.items():
                print "[%s]:[%s]" % (k, v)

            global server_debugmode
            server_debugmode = request.args['logging_mode'][0]


        #return """
        #<html>
        #<body>You submitted: %s</body>
        #</html>
        #""" % ("\r\n".join(request.content))

        return redirectTo("/config", request)


class StatusPage(Resource):
    # TODO: Add class comment here
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        # global only needed when global var value needs to change
        global server_number_of_views
        #server_starttime
        #server_debugmode

        server_number_of_views += 1

        responseBody = ""

        for k, v in server_vars.items():
            # value is returned as a list string ['string'], convert to only a string
            if type(v) == 'list':
                v = v[0]
            responseBody += ("<h3>%s : </h3>%s" % (k, v))

            txpower = True

            print "process.poll()"
            try:
                if fm_process.poll() is not None:
                    print "process pid[%d] have terminated with exitcode [%d]" % (fm_process.pid, fm_process.poll())
                    txpower = False
            except TypeError:
                print "process pid[%d] have not yet terminated" % (fm_process.pid)

        return "<title>Status Page</title><html><body><h1>%s</h1>" \
               "<h2>Web Server Parameters</h2>" \
               "<h3>Server Started                : </h3>%s" \
               "<h3>Running Time                  : </h3>%s" \
               "<h3>Number of Views               : </h3>%d" \
               "<h3>Debug Mode                    : </h3>%s" \
               "<h3>Transmitter powered on        : </h3>%s" \
               "<h3>piFM process identifier (pid) : </h3>%s" \
               "<h2>Transmitter Parameters</h2>" \
               "%s" \
               "</body></html>" % ("Status Page", server_starttime.strftime("%Y-%M-%d %H:%M:%S"),
                                   datetime.now() - server_starttime, server_number_of_views,
                                   server_debugmode, txpower, fm_process.pid if txpower else "None", responseBody)

#server_txmode = server_txmode_string[0]

#server_fixedstart = 1000000
#server_fixedstop = 1200000
#server_hopdelay = 200

#server_sweepstart = 1000000
#server_sweepstop = 1200000


class FormPage(Resource):
    # TODO: Add class comment here
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)
        print "FormPage:__init__"

    def render_GET(self, request):
        print "FormPage::render_GET"
        global server_number_of_views
        server_number_of_views += 1
        print "Number of GETs [%d]" % server_number_of_views
        #return """
        #<html>
        #<body>
        #<form method="POST">
        #<input name="form-field" type="text" />
        #<input type="submit" />
        #</form>
        #</body>
        #</html>
        #"""

        # TODO: Dynamically display page based on server variables
        return """
        <title>Transmit Page</title>
        <h1>Transmit Page</h1>
        <form method="post"

         <fieldset>
          <h2>Transmit Mode</h2>
          <p><label> <input type=radio name=%s required value="%s"> %s </label></p>
          <p><label> <input type=radio name=%s required value="%s"> %s </label></p>
          <p><label> <input type=radio name=%s required value="%s"> %s </label></p>
          <p><label> <input type=radio name=%s required value="%s"> %s </label></p>
         </fieldset>


         <h2>Fixed Frequency</h2>
         <p><label>Fstart(Hz) <input name="%s" value=%s required></label></p>
         <p><label>Fstop(Hz)  <input name="%s" value=%s required></label></p>
         <p><label>Delay(ms)  <input name="%s" value=%s required></label></p>

         <h2>Sweep Frequency</h2>
         <p><label>Fstart <input name="%s" value=%s  required></label></p>
         <p><label>Fstop <input name="%s"  value=%s required></label></p>

         <p><button>Submit</button></p>
        </form>
        """ % (server_varheader[0], server_txmode_string[0], server_txmode_string[0],
               server_varheader[0], server_txmode_string[1], server_txmode_string[1],
               server_varheader[0], server_txmode_string[2], server_txmode_string[2],
               server_varheader[0], server_txmode_string[3], server_txmode_string[3],
               server_varheader[1], server_vars[server_varheader[1]],
               server_varheader[2], server_vars[server_varheader[2]],
               server_varheader[3], server_vars[server_varheader[3]],
               server_varheader[4], server_vars[server_varheader[4]],
               server_varheader[5], server_vars[server_varheader[5]]
               )

    def render_POST(self, request):
        global fm_process
        print "FormPage::render_POST"

        print "Methods and Attributes of request"
        for i in request.__dict__:
            print "[%s]:[%s]" % (i, getattr(request, i))

        print "Request.args:"
        if request.args is not None:
            for k, v in request.args.items():
                print "[%s]:[%s]:[%s]" % (k, v, k in server_vars)

                #if type(v) == type([0]):
                if isinstance(v, type([0])):
                    j = v[0]
                else:
                    j = v

                # test if key is in server variable dictionary
                if k in server_vars:
                    # key exists in dictionary so go ahead and set
                    # set dictionaries key k to value v
                    server_vars[k] = j

        # test if transmitter must be switched on or off
        if server_vars[server_varheader[0]] == server_txmode_string[3]:
            # transmitter must be switched off
            print "Switch off transmitter"

            #test if fm_process exists
            if fm_process is not None:
                print "Terminating process pid[%d]" % fm_process.pid
                fm_process.terminate()

        if server_vars[server_varheader[0]] == server_txmode_string[0]:
            # transmitter must be switched on in Fixed Frequency mode
            print "Switch on transmitter in fixed frequency mode"
            runprun_pifm()

        if server_vars[server_varheader[0]] == server_txmode_string[1]:
            # transmitter must be switched on in Fixed Frequency mode
            print "Switch on transmitter in sweep frequency mode"
            runprun_pifm()

        if server_vars[server_varheader[0]] == server_txmode_string[2]:
            # transmitter must be switched on in Fixed Frequency mode
            print "Switch on transmitter in sweep frequency mode"
            runprun_pifm()

        #print "Request type = [%s]" % type(request)
        #print request


        request
        #return """
        #<html>
        #<body>You submitted: %s</body>
        #</html>
        #""" % (cgi.escape(request.args["form-field"][0]),)
#        return """
#        <html>
#        <body>You submitted: %s</body>
#        </html>
#        """ % ("\r\n".join(request.content))

        return redirectTo("/transmit", request)

# TODO: Refactor this class's name
class CalendarHome(Resource):
    # TODO: Add class comment here
    def getChild(self, name, request):
        if name == '':
            return self
        if name == 'about':
            return AboutPage()
        if name == 'status':
            return StatusPage()
        if name == 'transmit':
            return FormPage()
        if name == 'config':
            return ConfigPage()

        if name.isdigit():
            return YearPage(int(name))
        else:
            return NoResource()

    def render_GET(self, request):
        return "<html><body>Welcome to the test transmitter website!" \
               "<h3>To see the status of the web server goto URL/status</h3>" \
               "<h3>To see a calendar rendered,         goto URL/year</h3>" \
               "<h3>To see transmitter input parameter form goto URL/transmit</h3>" \
               "</body></html>"

# TODO: if __name__ == __main"__ here

port_number = 8000
server_starttime = datetime.today()

print "Started handle_post1.py"
print "Listening on port [%d]" % port_number
print "Start time : %s" % server_starttime.strftime("%Y-%M-%d %H:%M:%S")

print "Starting pifm"
runprun_pifm()
print "process.poll()"
try:
    print "process pid[%d] have terminated with exitcode [%d]" % (fm_process.pid, fm_process.poll())
except TypeError:
    print "process pid[%d] have not yet terminated" % (fm_process.pid)

server_starttime.strftime

root = CalendarHome()
factory = Site(root)
reactor.listenTCP(port_number, factory)

print "About to reactor.run()"
reactor.run()

print "Stopped handle_post1.py"