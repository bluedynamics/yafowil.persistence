yafowil.persistence
===================

Imports::

    >>> import yafowil.loader
    >>> import yafowil.persistence
    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller
    >>> from node.utils import instance_property

Form creation helper::

    >>> def create_form(instance, persist):
    ...     form = factory(
    ...         'form',
    ...         name='persistenceform',
    ...         props={
    ...             'action': 'http://example.com/form',
    ...             'persist': persist,
    ...         })
    ...     form['field1'] = factory('text')
    ...     form['field2'] = factory('text')
    ...     form['save'] = factory(
    ...         'submit',
    ...         props={
    ...             'action': 'save',
    ...             'expression': True,
    ...             'handler': instance.save,
    ...             'label': 'Save'
    ...         })
    ...     return form

Attribute Persistence
---------------------

Persist form data on object attributes.

Persitent object dummy::
    
    >>> class PersistentObject(object):
    ...     def __init__(self):
    ...         self.field1 = 'Init Val 1'
    ...         self.field2 = 'Init Val 2'

Form context class. Usually a zope browser page or pyramid view as class or
similar::

    >>> class AttributePersistingFormContext(
    ...     yafowil.persistence.PersistenceFormMixin):
    ... 
    ...     def form(self):
    ...         return create_form(
    ...             self, yafowil.persistence.attribute_persistence)
    ...     
    ...     @instance_property
    ...     def persistence_context(self):
    ...         return PersistentObject()

Instanciate::

    >>> form_context = AttributePersistingFormContext()
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
    'Init Val 1'
    
    >>> form_context.persistence_context.field2
    'Init Val 2'

Controller performs at init time. Data gets written to persistence context
by ``yafowil.persistence.PersistenceFormMixin.save`` with persist callback
defined in yafowil form::

    >>> controller = Controller(form, request)
    
    >>> form_context.persistence_context.field1
    'Value 1'
    
    >>> form_context.persistence_context.field2
    'Value 2'


Node Attribute persistence
--------------------------

Persist form data on node attributes::
    
    >>> from node.base import AttributedNode
    
    >>> class NodePersistingFormContext(
    ...     yafowil.persistence.PersistenceFormMixin):
    ... 
    ...     def form(self):
    ...         return create_form(
    ...             self, yafowil.persistence.node_persistence)
    ...     
    ...     @instance_property
    ...     def persistence_context(self):
    ...         node = AttributedNode()
    ...         node.attrs['field1'] = 'Init Val 1'
    ...         node.attrs['field2'] = 'Init Val 2'
    ...         return node

    >>> form_context = NodePersistingFormContext()
    >>> form_context.persistence_context.attrs['field1']
    'Init Val 1'
    
    >>> form_context.persistence_context.attrs['field2']
    'Init Val 2'
    
    >>> controller = Controller(form_context.form(), request)
    
    >>> form_context.persistence_context.attrs['field1']
    'Value 1'
    
    >>> form_context.persistence_context.attrs['field2']
    'Value 2'


Dict persistence
----------------

Persist form data on dict like object::
    
    >>> class DictPersistingFormContext(
    ...     yafowil.persistence.PersistenceFormMixin):
    ... 
    ...     def form(self):
    ...         return create_form(
    ...             self, yafowil.persistence.dict_persistence)
    ...     
    ...     @instance_property
    ...     def persistence_context(self):
    ...         return {'field1': 'Init Val 1', 'field2': 'Init Val 2'}

    >>> form_context = DictPersistingFormContext()
    >>> form_context.persistence_context['field1']
    'Init Val 1'
    
    >>> form_context.persistence_context['field2']
    'Init Val 2'
    
    >>> controller = Controller(form_context.form(), request)
    
    >>> form_context.persistence_context['field1']
    'Value 1'
    
    >>> form_context.persistence_context['field2']
    'Value 2'
