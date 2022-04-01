import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class AuthenticationLog(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(required=True)
    login_time = columns.DateTime(required=True)
