# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from pd.prenotazioni.browser.prenotazione_add import AddForm as BaseForm
from plone.app.form.validators import null_validator
from plone.memoize.view import memoize
from rg.prenotazioni import prenotazioniMessageFactory as _
from urllib import urlencode
from zope.formlib.form import action, setUpWidgets


class AddForm(BaseForm):
    """ Customize pd.prenotazioni add form to redirect to another page
    """
    template = ViewPageTemplateFile('prenotazione_add.pt')

    banned_redirect_keys = (
        '_authenticator',
        'ajax_include_head',
        'ajax_load',
        'form..hashkey',
        'form.actions.book',
        'form.captcha',
        'form.tipology-empty-marker',
    )

    @property
    @memoize
    def form_fields(self):
        '''
        The fields for this form
        '''
        ff = super(AddForm, self).form_fields
        ff.omit('captcha')
        return ff

    def setUpWidgets(self, ignore_request=False):
        '''
        From zope.formlib.form.Formbase.
        '''
        self.adapters = {}
        fieldnames = [x.__name__ for x in self.form_fields]
        data = {}
        for key in fieldnames:
            value = self.request.form.get(key)
            if value is not None and not value == u'':
                data[key] = value
                self.request[key] = value

        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request,
            data=data)

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
        target = 'http://example.com/?%s' % urlencode(params)
        return self.request.response.redirect(target)

    @action(_(u"action_cancel", default=u"Cancel"), validator=null_validator, name=u'cancel')  # noqa
    def action_cancel(self, action, data):
        '''
        Cancel
        '''
        target = self.back_to_booking_url
        return self.request.response.redirect(target)
