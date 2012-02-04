yafowil.persistence
===================

::
    >>> import yafowil.loader
    >>> import yafowil.persistence
    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller
    >>> from node.utils import instance_property


Attribute Persistence
---------------------

Persitent object dummy::
    
    >>> class PersistentObject(object):
    ...     def __init__(self):
    ...         self.field1 = None
    ...         self.field2 = None

Form context class. Usually a browser page (zope) or pyramid view as class or
similar::

    >>> class PersistingFormContext(yafowil.persistence.PersistenceFormMixin):
    ...     def form(self):
    ...         form = factory(
    ...             'form',
    ...             name='persistenceform',
    ...             props={
    ...                 'action': 'http://example.com/form',
    ...                 'persist': yafowil.persistence.attribute_persistence,
    ...             })
    ...         form['field1'] = factory('text')
    ...         form['field2'] = factory('text')
    ...         form['save'] = factory(
    ...             'submit',
    ...             props={
    ...                 'action': 'save',
    ...                 'expression': True,
    ...                 'handler': self.save,
    ...                 'label': 'Save'
    ...             })
    ...         return form
    ...     
    ...     @instance_property
    ...     def persistence_context(self):
    ...         return PersistentObject()

Instanciate::

    >>> form_context = PersistingFormContext()
    >>> form_context.persistence_context
    <PersistentObject object at ...>
    
    >>> form = form_context.form()
    >>> form
    <Widget object 'persistenceform' at ...>
    
    >>> request = dict()
    >>> request['action.persistenceform.save'] = '1'
    >>> request['persistenceform.field1'] = 'Value 1'
    >>> request['persistenceform.field2'] = 'Value 2'

Form was not processed yet. No data on persistence context::

    >>> form_context.persistence_context.field1
    
    >>> form_context.persistence_context.field2

Controller performs at init time. Data gets written to persistence context
by ``yafowil.persistence.PersistenceFormMixin.save`` with persist callback
defined in yafowil form::

    >>> controller = Controller(form, request)
    
    >>> form_context.persistence_context.field1
    'Value 1'
    
    >>> form_context.persistence_context.field2
    'Value 2'
