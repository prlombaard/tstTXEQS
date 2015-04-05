__author__ = '0400428'

#Example 4-8. handle_post.py

from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from calendar import calendar
from datetime import datetime, date, time

# global module variables
server_state = ""
server_starttime = datetime.today()
server_number_of_views = 0

class YearPage(Resource):
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        global server_number_of_views
        server_number_of_views += 1

        return "<html><body><pre>%s</pre></body></html>" % (calendar(self.year),)


class AboutPage(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        global server_number_of_views
        server_number_of_views += 1

        return "<html><body><pre>%s</pre></body></html>" % ("About this page",)


class StatusPage(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        global server_number_of_views
        global server_starttime
        server_number_of_views += 1

        return "<html><body><h1>%s</h1>" \
               "<h2>Server Started                : %s</h2>" \
               "<h2>Running Time [HH:MM:ss.mmmmm] : %s</h2>" \
               "<h2>Number of Views               : %d</h2>" \
               "</body></html>" % ("Status Page", server_starttime.strftime("%Y-%M-%d %H:%M:%S"), datetime.now() - server_starttime, server_number_of_views)


class FormPage(Resource):
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)
        print "FormPage:__init__"

    def __del__(self):
        print "FormPage:__del__"

    def getChild(self, name, request):
        print "FormPage:getChild"
        if name == '':
            return self
        if name.isdigit():
            return YearPage(int(name))
        else:
            return NoResource()

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
        <form method="post"

         <fieldset>
          <legend> Mode </legend>
          <p><label> <input type=radio name=mode required value="fixed freq"> Fixed Frequency </label></p>
          <p><label> <input type=radio name=mode required value="sweep freq"> Sweep Frequency </label></p>
          <p><label> <input type=radio name=mode required value="freq hop">   Hop Frequency </label></p>
         </fieldset>


         <h1>Fixed Frequency</h1>
         <p><label>Fstart(Hz) <input name="fixedstart" minlength=6 value=1000000 required></label></p>
         <p><label>Fstop(Hz)  <input name="fixedstop"  value=1200000 required></label></p>
         <p><label>Delay(ms)  <input name="hopdelay" value=200     required></label></p>

         <h1>Sweep Frequency</h1>
         <p><label>Fstart <input name="sweepstart" value=1000000  required></label></p>
         <p><label>Fstop <input name="sweepstop"   value=1200000 required></label></p>

         <fieldset>
          <legend> CGI Debug Mode</legend>
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

class CalendarHome(Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        if name == 'about':
            return AboutPage()
        if name == 'status':
            return StatusPage()
        if name == 'transmit':
            return FormPage()
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