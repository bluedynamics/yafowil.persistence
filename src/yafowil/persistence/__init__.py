

def attribute_persistence(widget, data, context):
    setattr(context, widget.name, data.extrated)


def node_persistence(widget, data, context):
    context.attrs[widget.name] = data.extracted


def dict_persistence(widget, data, context):
    context[widget.name] = data.extracted


class PersistenceFormMixin(object):

    @property    
    def persistence_context(self):
        return self.context
    
    def save(self, widget, data):
        global_persistence = widget.attrs["persistence"]
        def persist_recursive(persistence, widget, data, context):
            if not widget.attrs.get('structural'):
                persistence(widget, data, context)
            for child in widget.values():
                if child.attrs.get('persistence'):
                    persistence = child.attrs['persistence']
                persist_recursive(persistence, child, data, context)
        persist_recursive(
            global_persistence, widget, data, self.persistence_context)
        