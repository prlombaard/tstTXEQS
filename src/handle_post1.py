#!/usr/bin/env python
# Network Controlled Pirate Radio using pifm
# Author: Rudolph Lombaard

__author__ = 'prlombaard@gmail.com'

"""
Original Source: Twisted Examples - e-book
                 Example 4-8. handle_post.py
"""

from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from calendar import calendar
from datetime import datetime
from twisted.web.util import redirectTo
import sys
from subprocess import Popen
from os import pipe, devnull
from time import sleep

# global module variables
server_state = ""
server_starttime = datetime.today()
server_number_of_views = 0

# TODO: #1, Load securely from config file
server_users_and_passwords = {'user': 'user', 'admin': 'admin'}
server_debugmode = "logging off"
server_txmode_string = ['Fixed Frequency', 'Sweep Frequency', 'Hop Frequency', 'Off']
server_varheader = ['txmode', 'fixedstart', 'fixedstop', 'hopdelay', 'sweepstart', 'sweepstop']
server_logging_mode = {'Append Log': 'Logging on', 'Rewrite log': 'Logging on', 'Off': 'Logging'}
server_vars = {server_varheader[0]: server_txmode_string[0], server_varheader[1]: 88900000, server_varheader[2]: 100000000, server_varheader[3]: 200, server_varheader[4]: 1000000, server_varheader[5]: 1200000}

# piFM related variables
# path for pifm executable
PIFM_BIN = "/boot/pirateradio/pifm"
music_pipe_r, music_pipe_w = pipe()
fm_process = None
frequency = 88.9
play_stereo = True

# TODO: #2, Add logging like in import logging


def isRunning(processid):
    try:
        if (processid.poll() is not None) or (processid is None):
            return False
        else:
            return True
    except TypeError as e1:
        return True
    except AttributeError as e2:
        return False


def run_pifm():
    global fm_process
    global frequency

    # TODO: #3, Only create, terminate process if transmitter parameters have changed

    # TODO: #4, Move the platform checking out of this method, use common array name in Popen, i.e. not hardcoded string literals
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
                # TODO: #8, Check how long to wait before creating new process
                sleep(1)

            print "Creating new process"
            # create process that takes input from the pipe "music_pipe_r" and output to null device (not to the screen)
            fm_process = Popen(["ping", "127.0.0.1", "-t"], stdin=music_pipe_r, stdout=dev_null)

            # create process that takes input from the pipe "music_pipe_r" and output the terminal (screen)
            #fm_process = Popen(["ping", "127.0.0.1", "-t"], stdin=music_pipe_r)

            print "fm process PID [%d]" % (fm_process.pid)
    else:
        print "Platform : Linux"
        with open(devnull, "w") as dev_null:
            # TODO: Temporary fix if os is Windows then use pipe otherwise use the real command assuming were on rPi platform
            # TODO: Bug, check if process already open, kill process then create new one
            print "run_pifm(): Frequency = [%0.2f]" % frequency
            fm_process = Popen([PIFM_BIN, "-", str(frequency), "44100", "stereo" if play_stereo else "mono"], stdin=music_pipe_r, stdout=dev_null)
            print "run_pifm():process created pid(%d)" % (fm_process.pid)
            #fm_process = Popen(["ping", "127.0.0.1"], stdin=music_pipe_r, stdout=dev_null)


class YearPage(Resource):
    """
    This class inherits from a twisted.web.resource class.
    This class returns a HTML page displaying a calendar of the year passed to the web resource as an argument
    """
    isLeaf = True

    def __init__(self, year):
        """
        Constructor method, calls the super class, then takes an integer year and assigns it to an instance variable.
        """
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        """
        This method is called when a GET request is sent from the browser.
        The global number of server views (GETS) is increased by one.
        Method returns an HTML string displaying a nicely rendered year calender
        """
        global server_number_of_views
        server_number_of_views += 1

        return "<title>Calender for %s</title><html><body><pre>%s</pre></body></html>" % (self.year,calendar(self.year))


class AboutPage(Resource):
    """
    This class inherits from a twisted.web.resource class.
    This class returns a HTML page displaying and about message for this website
    """
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        """
        This method is called when a GET request is sent from the browser.
        The global number of server views (GETS) is increased by one.
        Method returns an HTML string displaying an about page.
        """
        global server_number_of_views
        server_number_of_views += 1

        return "<html><body><pre>%s</pre></body></html>" % ("About this page",)


class ConfigPage(Resource):
    """
    This class inherits from a twisted.web.resource class.
    This class returns a HTML page displaying a form containing configuration fields that modifies the web servers internal configuration.
    """
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        """
        This method is called when a GET request is sent from the browser.
        The global number of server views (GETS) is increased by one.
        Method returns an HTML string displaying a form containing configuration fields
        """
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
        """
        This method is called when a POST request is sent from the browser; i.e. when the submit button have been clicked
        The global number of server views (GETS) is increased by one.
        Method redirects the browser to the URI /config.
        This generates a GET request which calls this classes render_GET method
        """
        print "TransmitPage::render_POST"

        print "Methods and Attributes of request"
        for i in request.__dict__:
            print "[%s]:[%s]" % (i, getattr(request, i))

        print "Request.args:"
        if request.args is not None:
            for k, v in request.args.items():
                print "[%s]:[%s]" % (k, v)

            global server_debugmode
            server_debugmode = request.args['logging_mode'][0]

            # TODO: #10, Add code to actually switch on/off logging modes

        return redirectTo("/config", request)


class StatusPage(Resource):
    """
    This class inherits from a twisted.web.resource class.
    This class returns a HTML page displaying the status of the web server and other piFM related information
    """
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        """
        This method is called when a GET request is sent from the browser.
        The global number of server views (GETS) is increased by one.
        Method returns a HTML string that displays the various global variable information nicely.
        """
        # global only needed when global var value needs to change
        global server_number_of_views

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
            # TODO: #11, Possible bug, Check these if statements, something tells me they are incorrectly written
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


class TransmitPage(Resource):
    """
    This class inherits from a twisted.web.resource class.
    This class returns a HTML page displaying a form containing fields that modifies the transmitter parameters of the server.
    """
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)
        print "TransmitPage:__init__"

    def render_GET(self, request):
        """
        This method is called when a GET request is sent from the browser.
        The global number of server views (GETS) is increased by one.
        Method returns a HTML string that displays a form with fields pertaining to the transmitter variables
        """
        print "TransmitPage::render_GET"
        global server_number_of_views
        server_number_of_views += 1
        print "Number of GETs [%d]" % server_number_of_views

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
        """
        This method is called when a POST request is sent from the browser; i.e. when the submit button have been clicked
        The global number of server views (GETS) is increased by one.
        Arguments are parsed from the request string.
        global server variables are modified accordingly.
        piFM process is started/stopped/changed depending on the Transmitter Mode field value
        Method redirects the browser to the URI /transmit.
        This generates a GET request which calls this classes render_GET method
        """
        global fm_process
        global frequency
        print "TransmitPage::render_POST"

        print "Methods and Attributes of request"
        for i in request.__dict__:
            print "[%s]:[%s]" % (i, getattr(request, i))

        # TODO: #12, Check validity of arguments before assigning to server variables

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

        # TODO: #?, Implement fixed frequency
        
        if server_vars[server_varheader[0]] == server_txmode_string[0]:
            # transmitter must be switched on in Fixed Frequency mode
            print "Switch on transmitter in fixed frequency mode"

            # Set broadcast frequency
            frequency = int(server_vars[server_varheader[1]]) / 1000000.0
            
            print "Frequency set to %0.2f" % frequency
            
            run_pifm()

        # TODO: #5, Implement frequency sweep mode

        if server_vars[server_varheader[0]] == server_txmode_string[1]:
            # transmitter must be switched on in Fixed Frequency mode
            print "Switch on transmitter in sweep frequency mode"
            
            run_pifm()
            

        # TODO: #6, Implement frequency hopper mode

        if server_vars[server_varheader[0]] == server_txmode_string[2]:
            # transmitter must be switched on in Fixed Frequency mode
            print "Switch on transmitter in sweep frequency mode"
            

            # TODO: use the hop delay server var instead of local temp variable
            # calculate hop delay
            hop_sleep = int(server_vars[server_varheader[3]]) / 1000
            hop_sleep = 1 if hop_sleep < 1 else hop_sleep
            
            print "Hopper delay %0.2f" % (hop_sleep)

            # Set broadcast frequency            
            # Create list of frequencies to hop over
            hop_set = [88.2, 88.9, 88.2, 88.9, 88.2]
            
            # Iterate though the list of hop frequencies
            for i in xrange(0,5):
                # Set hopping emission broadcast frequency
                #frequency = int(server_vars[server_varheader[1]]) / 1000000.0
                frequency = hop_set[i]
                
                print "Frequency set to %0.2f" % frequency
                
                # activate transmission
                run_pifm()
                
                # sleep for hop delay, so transmission is active for hop_delay seconds
                # TODO: use a better sleep function than have sub 1 second resolution
                sleep(hop_sleep)
                
                # terminate transmission
                print "Terminating process pid[%d]" % fm_process.pid
                fm_process.terminate()
                
                sleep(1)

        return redirectTo("/transmit", request)


class HomePage(Resource):
    """
    This class inherits from a twisted.web.resource class.
    This class is the root URI web resource. It instantiates other classes based on the URL requested
    """
    def getChild(self, name, request):
        """
        This method get called when a request comes in from a browser
        This method then decides based on the requested URI which twisted.web.resource class to instantiate to process the GET/POST requests
        """
        if name == '':
            # root URI requested "http://IP:port/" or "http://IP:port"
            return self
        if name == 'about':
            # about URI requested "http://IP:port/about"
            return AboutPage()
        if name == 'status':
            # about URI requested "http://IP:port/status"
            return StatusPage()
        if name == 'transmit':
            # about URI requested "http://IP:port/transmit"
            return TransmitPage()
        if name == 'config':
            # about URI requested "http://IP:port/config"
            return ConfigPage()
        if name.isdigit():
            # about URI requested "http://IP:port/digit"
            return YearPage(int(name))
        else:
            # invalid URI requested so return a error web resource with renders an HTML that displays a default 404 message
            return NoResource()

    def render_GET(self, request):
        """
        This method is called when a GET request is sent from the browser to the URI "/" i.e. root page
        Root page such as IP:8000/
        The global number of server views (GETS) is increased by one.
        Method returns a HTML string that displays a welcome message
        """
        return "<html><body>Welcome to the test transmitter website!" \
               "<h3>To see the status of the web server goto URL/status</h3>" \
               "<h3>To see a calendar rendered,         goto URL/year</h3>" \
               "<h3>To see transmitter input parameter form goto URL/transmit</h3>" \
               "</body></html>"

# TODO: #7, if __name__ == __main"__ here

# TODO: Implement argument parsing, linux style help in the command line

# Web Server listening socket port to bind to
port_number = 8000

# Time when the Web server is started
server_starttime = datetime.today()

print "Started handle_post1.py"
print "Listening on port [%d]" % port_number
print "Start time : %s" % server_starttime.strftime("%Y-%M-%d %H:%M:%S")

print "Starting pifm"
run_pifm()
print "process.poll()"
try:
    print "process pid[%d] have terminated with exitcode [%d]" % (fm_process.pid, fm_process.poll())
except TypeError:
    print "process pid[%d] have not yet terminated" % (fm_process.pid)

root = HomePage()
factory = Site(root)
reactor.listenTCP(port_number, factory)

print "About to reactor.run()"
reactor.run()

print "Stopped handle_post1.py"
