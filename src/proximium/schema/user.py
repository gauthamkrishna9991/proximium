import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class User(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    username = columns.Text(index=True)
    password_salt = columns.Blob(required=True)
    password_hash = columns.Blob(required=True)
