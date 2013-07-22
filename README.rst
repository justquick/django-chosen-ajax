Overview
==================

.. image:: http://i.imgur.com/FWNIt7L.jpg?2
   :width: 320px
   
.. image:: http://i.imgur.com/wK54oJF.jpg?1
   :width: 320px

:Author:
   Eric Honkanen <eric@epicowl.com>
:Version: 0.1.0

django-chosen-ajax implements the `chosen <http://harvesthq.github.io/chosen/>`_ javascript library into the django admin for select form elements. It also implements ajax autocomplete functionality for form fields which have large numbers of related objects. The library currently uses `jquery <http://www.jquery.com>`_ and was inspired by `django-chosen <https://github.com/theatlantic/django-chosen>`_ and `chosen-ajax <https://github.com/meltingice/ajax-chosen>`_.

Features
--------

- Integrates `chosen <http://harvesthq.github.io/chosen/>`_ into the admin
- Implements ajax functionality for ModelMultipleChoiceField's


Install
-------

Install with pip

::

    pip install git+https://github.com/epicowl/django-chosen-ajax.git#egg=django-chosen-ajax

Add ``chosen`` to your ``INSTALLED_APPS``

Run ``collectstatic``

Compatibility
^^^^^^^^^^^^^

django-chosen-ajax has been tested with

:Django: 1.4, 1.5
:Python: 2.7
:Database: PostgreSQL

Usage
------

Subclass the ChosenAdminForm using the ChosenAjaxField for ajax fields and include the required ``search_fields=('field',)``

.. code-block:: python

    from chosen.forms import ChosenAdminForm
    from chosen.fields import ChosenAjaxField


    class PonyForm(ChosenAdminForm):
        ponies = ChosenAjaxField(
            required=False, 
            queryset=Pony.objects.all(), 
            search_fields=('name', 'breed',)
        )

        class Meta:
            model = YourModel


Currently you will also have to add the admin site to your ModelAdmin to make the green add related button work.

.. code-block:: python

    from django.contrib import admin
    from ponyapp.forms import PonyForm


    class PonyAdmin(admin.ModelAdmin):
        form = PonyForm

        def __init__(self, model, admin_site):
            super(PonyAdmin, self).__init__(model, admin_site)
            self.form.admin_site = admin_site


You can add as many fields to search_fields as you need, they get combined into a lookup. Everything else is automatic and handled in the ChosenAdminForm.

Hit me up if you have questions or want to contribute!

