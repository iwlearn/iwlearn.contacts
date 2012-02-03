import urllib, urllib2
try:
    import simplejson as json
except ImportError:
    import json

import cgi
import logging

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _

from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle

from adrview import AdrView

logger = logging.getLogger('iwlearn.contacts')

class IAddCoordsView(Interface):
    """
    AddCoords view interface
    """



class AddCoordsView(BrowserView):
    """
    AddCoords browser view
    """
    implements(IAddCoordsView)

    url = 'http://wherein.yahooapis.com/v1/document'

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def make_place(self, brain):
        ob = brain.getObject()
        url = brain.getURL() + '/@@adr_view.html'
        view = cgi.escape(AdrView(ob, self.request)()).encode(
                                    'ascii', 'xmlcharrefreplace')
        params = {'outputType': 'json',
            #'documentURL': url,
            'documentContent': view,
            'documentType': 'text/html',
            'appid': 'pySuZD7V34FHjlmmw72YPBBf4R55MwkhtNCo_c3fR1aQY4wNKsU6YevDnyPSwJ53uu3SlwvPifbaWjUCfMu_umRPPGk-',
            }
        try:
            params = urllib.urlencode(params)
        except:
            logger.error(brain.Title + ': error encoding org')
            return brain.Title + ': Error setting coordinates'
        #try:
        response = urllib2.urlopen(self.url, params)
        #except urllib2.HTTPError, e:
            # Check for for Forbidden HTTP status, which means invalid API key.
       #     if e.code == 403:
       #         return ['Invalid API key.']
       #     return ['error %i' % e.code]

        output = json.loads(response.read())
        try:
            logger.info(brain.Title + ': ' +
                str(output['document']['extents']['center']))
            geo = IGeoManager(ob)
            print geo.isGeoreferenceable()
            lat = float(output['document']['extents']['center']['latitude'])
            lon = float(output['document']['extents']['center']['longitude'])
            geo.setCoordinates('Point', (lon, lat))
            return brain.Title + str(output['document']['extents']['center'])
        except:
            logger.error(brain.Title + ': ' + str(output))
            return brain.Title + ': Error setting coordinates'



    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_coords(self):
        brains = self.portal_catalog(Type = 'ContactOrganization')
        results = []
        for brain in brains:
            if not brain.zgeo_geometry:
                 results.append(self.make_place(brain))
            else:
                if not brain.zgeo_geometry['coordinates']:
                    results.append(self.make_place(brain))

        return results
