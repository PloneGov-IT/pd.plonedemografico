# -*- coding: utf-8 -*-
from pd.prenotazioni.browser.prenotazione_add import AddForm as BaseForm
from plone.app.form.validators import null_validator
from rg.prenotazioni import prenotazioniMessageFactory as _
from urllib import urlencode
from zope.formlib.form import action


class AddForm(BaseForm):
    """ Customize pd.prenotazioni add form to redirect to another page
    """
    banned_redirect_keys = (
        '_authenticator',
        'form..hashkey',
        'form.actions.book',
        'form.captcha',
        'form.tipology-empty-marker',
    )

    @action(_('action_book', u'Book'), name=u'book')
    def action_book(self, action, data):
        '''
        Book this resource
        '''
        obj = self.do_book(data)
        obj  # pyflakes
        params = self.request.form.copy()
        for key in self.banned_redirect_keys:
            params.pop(key, None)
        import pdb;pdb.set_trace()
        target = 'http://example.com/?%s' % urlencode(params)
        return self.request.response.redirect(target)

    @action(_(u"action_cancel", default=u"Cancel"), validator=null_validator, name=u'cancel')  # noqa
    def action_cancel(self, action, data):
        '''
        Cancel
        '''
        target = self.back_to_booking_url
        return self.request.response.redirect(target)
