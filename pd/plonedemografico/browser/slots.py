# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Five.browser import BrowserView
from json import dumps, JSONEncoder
from plone import api
from rg.prenotazioni.adapters.slot import BaseSlot


class SlotAwareEncoder(JSONEncoder):
    ''' Return an Encoder that knows about slots
    '''
    def default(self, obj):
        if isinstance(obj, BaseSlot):
            return obj.start()
        return super(SlotAwareEncoder, self).default(obj)


class View(BrowserView):
    ''' Return tipologies jsonified
    '''

    def __call__(self):
        '''
        '''
        prenotazioni = api.content.get_view('prenotazioni_context_state',
                                            self.context,
                                            self.request)
        booking_date = self.request.form.get('booking_date',
                                             DateTime()).asdatetime().date()
        booking_urls = prenotazioni.get_all_booking_urls(booking_date)
        url_lists = []
        for key in booking_urls:
            url_lists.append([url['url'] for url in booking_urls[key]])
        self.request.response.setHeader('Content-Type', 'application/json')
        return dumps(url_lists, cls=SlotAwareEncoder)
