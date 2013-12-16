# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from rg.prenotazioni.browser.prenotazioni_context_state import PrenotazioniContextState as BaseView  # noqa


class PrenotazioniContextState(BaseView):
    ''' This customizes prenotazioni context state
    '''
    @property
    @memoize
    def add_view(self):
        ''' We want to control the view that allows us to book stuff

        If the parameter form.add_view is not passed we just return
        the parent's one
        '''
        add_view = self.request.form.get('form.add_view', '')
        if not add_view:
            add_view = BaseView.add_view
        elif isinstance(add_view, list):
            add_view = add_view[0]
            self.request.form['form.add_view'] = add_view
        return add_view
