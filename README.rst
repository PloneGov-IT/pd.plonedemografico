.. contents::

Introduction
============

Add custom views to the Plone booking product `pd.prenotazioni`__.

__ https://pypi.python.org/pypi/pd.prenotazioni

The functionality of this package will be merged in
`pd.prenotazioni`__.

__ https://pypi.python.org/pypi/pd.prenotazioni


The views
=========

prenotazione_add_ro
-------------------

This is a form with all fields hidden.
It is meant to be used to display the data before final submission.

prenotazioni_context_state
--------------------------

Extends the `rg.prenotazioni homonymous view`__ in order to override
the attribute ``add_view``.
If a parameter called ``form.add_view`` is passed, it will be used
as the add form for a booking object.

We use this in combination with an apache rewrite rule that injects in the
request the parameter with the value ``prenotazioni_add_ro``::

    RewriteCond %{QUERY_STRING} !((.*)form_add_view=(.*))
    RewriteRule ^/path_to_enable_custom_form/(.*) /notheme/$1?form.add_view=prenotazione_add_ro [QSA]

__ https://github.com/PloneGov-IT/rg.prenotazioni/blob/master/rg/prenotazioni/browser/prenotazioni_context_state.py#L59



slots.json
----------

Call this view like this:

- http://localhost:8080/Plone/agenda/slots.json?booking_date=2014/06/23

It will return a list of urls::

    [
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+09%3A00&",
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+09%3A05&",
        ...
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+17%3A50&",
        "http://localhost:8080/Plone/agenda/prenotazione_add?form.booking_date=2014-06-23+17%3A55&"
    ]

If the parameter ``booking_date`` is not specified it will default to today.


tipologies.json
---------------

Call this view like this:

- http://localhost:8080/Plone/agenda/@@tipologies.json

It will return a json object::

    {
        "Task for 1 person": 10,
        "Task for 2 people": 20,
        "Task for 3 people": 30
     }

The key is the booking tipology name,
the value the booking duration in minutes.

Credits
=======

Developed with the support of `Comune di Padova`__.

Comune di Padova supports the `PloneGov initiative`__.

.. image:: https://raw.githubusercontent.com/PloneGov-IT/pd.prenotazioni/master/docs/logo-comune-pd-150x200.jpg
   :alt: Comune di Padova's logo

__ http://www.padovanet.it/
__ http://www.plonegov.it/


Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
      :target: http://www.redturtle.it/