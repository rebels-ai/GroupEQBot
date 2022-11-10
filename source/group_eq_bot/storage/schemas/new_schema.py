from datetime import datetime
from elasticsearch_dsl import Document, InnerDoc, Text, Long, Date, Object


class NestedDoc(InnerDoc):
    parameter1 = Text()

class NewSchema(Document):
    chat_id = Long()
    created_date = Date()

    def save(self, ** kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(** kwargs)
