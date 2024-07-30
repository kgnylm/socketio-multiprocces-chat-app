from datetime import datetime

import mongoengine as me


class LogModel(me.Document):
    meta = {
        "collection": "logs",
        "ordering": ["-created_at"],
    }
    username = me.StringField(min_length=1)
    message = me.StringField(min_length=1)
    type = me.StringField(min_length=1)
    created_at = me.DateTimeField(default=datetime.now)
    is_read = me.BooleanField(default=False)

    def save(self, *args, **kwargs):
        return super(LogModel, self).save(*args, **kwargs)
