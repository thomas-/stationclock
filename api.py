from twisted.web.resource import Resource
from twisted.web.server import Site
from utils import send_event
from settings import ALLOWED_IPS


class ProtectedSite(Site):
    def buildProtocol(self, addr):
	print addr.host
        if addr.host in ALLOWED_IPS:
            return Site.buildProtocol(self, addr)
        else:
            return None


class SongResource(Resource):
    def render_POST(self, request):
        #super(SongResource, self).render_POST(request)
        artist = request.args['artist'][0]
        title = request.args['title'][0]
        length = int(float(request.args['length'][0]))
        send_event(event='song', artist=artist, title=title, length=length)
        return 'OK'


class StopResource(Resource):
    def render_GET(self, request):
        send_event(event='stop')
        return 'OK'


class AnnouncementResource(Resource):
    def render_POST(self, request):
        event_dict = {'event': 'announcement'}
        for k, v in request.args.items():
            event_dict.update({k: v[0]})
        send_event(**event_dict)
        return 'OK'


class InfoResource(Resource):
    def render_POST(self, request):
        event_dict = {'event': 'info'}
        for k, v in request.args.items():
            event_dict.update({k: v[0]})
            # send_event(eventrequest.args['show'][0]
            # event_dict.update({'show': request.args['show'][0]})
            # event_dict.update({'onair': request.args['onair'][0]})
        send_event(**event_dict)
        return 'OK'

root = Resource()
root.putChild('announcement', AnnouncementResource())
root.putChild('play', SongResource())
root.putChild('stop', StopResource())
root.putChild('info', InfoResource())
