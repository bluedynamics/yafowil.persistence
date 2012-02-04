def attribute_persistence(widget, data, context):
    """Persist extracted widget data on object attribute.
    """
    setattr(context, widget.name, data.extracted)


def node_persistence(widget, data, context):
    """Persist extracted widget data on node.attrs.
    """
    context.attrs[widget.name] = data.extracted


def dict_persistence(widget, data, context):
    """Persist extracted widget data via __setitem__.
    """
    context[widget.name] = data.extracted


def persist_leafs(widget, data, context):
    """Default persisting behavior.
    
    Persistence callback is executed with all leaf widgets.
    """
    def walk(persist, widget, data, context):
        children = widget.values()
        if not widget.attrs.get('structural') and not children:
            persist(widget, data.fetch(widget.dottedpath), context)
        for child in children:
            if child.attrs.get('persist'):
                persist = child.attrs['persist']
            walk(persist, child, data, context)
    walk(widget.attrs['persist'], widget, data, context)


class PersistenceFormMixin(object):
    """Mixin for form context implementing classes.
    """

    @property
    def persistence_context(self):
        """Context which represents persistent object.
        """
        return self.context
    
    def save(self, widget, data):
        """Form save action callback.
        """
        persist_leafs(widget, data, self.persistence_context)