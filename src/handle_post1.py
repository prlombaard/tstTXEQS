__author__ = '0400428'

#Example 4-8. handle_post.py

from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from calendar import calendar
from datetime import datetime, date, time

# global module variables
# TODO: Add server global variables here
server_state = ""
server_starttime = datetime.today()
server_number_of_views = 0

# TODO: Load securely from config file
server_users_and_passwords = {'user': 'user', 'admin': 'admin'}
server_debugmode = "logging off"
server_modes = ['Fixed Frequency', 'Sweep Frequency', 'Hop Frequency']
server_vars = {'txmode': server_modes[0], 'fixedstart': 1000000, 'fixedstop': 1200000, 'hopdelay': 200, 'sweepstart': 1000000, 'sweepstop': 1200000}


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


        return """
        <html>
        <body>You submitted: %s</body>
        </html>
        """ % ("\r\n".join(request.content))



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

        return "<title>Status Page</title><html><body><h1>%s</h1>" \
               "<h2>Web Server Parameters</h2>" \
               "<h3>Server Started                : </h3>%s" \
               "<h3>Running Time                  : </h3>%s" \
               "<h3>Number of Views               : </h3>%d" \
               "<h3>Debug Mode                    : </h3>%s" \
               "<h2>Transmitter Parameters</h2>" \
               "<h3>Transmit Mode                 : </h3>%s" \
               "<h3>Fixed Frequency Start         : </h3>%s" \
               "<h3>Fixed Frequency Stop          : </h3>%s" \
               "</body></html>" % ("Status Page", server_starttime.strftime("%Y-%M-%d %H:%M:%S"),
                                   datetime.now() - server_starttime, server_number_of_views,
                                   server_debugmode, server_txmode, server_fixedstart, server_fixedstop)
server_txmode = server_modes[0]

server_fixedstart = 1000000
server_fixedstop = 1200000
server_hopdelay = 200

server_sweepstart = 1000000
server_sweepstop = 1200000


class FormPage(Resource):
    # TODO: Add class comment here
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)
        print "FormPage:__init__"

    def __del__(self):
        print "FormPage:__del__"

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

        return """
        <title>Transmit Page</title>
        <h1>Transmit Page</h1>
        <form method="post"

         <fieldset>
          <h2>Transmit Mode</h2>
          <p><label> <input type=radio name=mode required value="fixed freq"> Fixed Frequency </label></p>
          <p><label> <input type=radio name=mode required value="sweep freq"> Sweep Frequency </label></p>
          <p><label> <input type=radio name=mode required value="freq hop">   Hop Frequency </label></p>
         </fieldset>


         <h2>Fixed Frequency</h2>
         <p><label>Fstart(Hz) <input name="fixedstart" minlength=6 value=1000000 required></label></p>
         <p><label>Fstop(Hz)  <input name="fixedstop"  value=1200000 required></label></p>
         <p><label>Delay(ms)  <input name="hopdelay" value=200     required></label></p>

         <h2>Sweep Frequency</h2>
         <p><label>Fstart <input name="sweepstart" value=1000000  required></label></p>
         <p><label>Fstop <input name="sweepstop"   value=1200000 required></label></p>

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
        #print "Request type = [%s]" % type(request)
        #print request


        request
        #return """
        #<html>
        #<body>You submitted: %s</body>
        #</html>
        #""" % (cgi.escape(request.args["form-field"][0]),)
        return """
        <html>
        <body>You submitted: %s</body>
        </html>
        """ % ("\r\n".join(request.content))

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

server_starttime.strftime

root = CalendarHome()
factory = Site(root)
reactor.listenTCP(port_number, factory)
reactor.run()

print "Stopped handle_post1.py"