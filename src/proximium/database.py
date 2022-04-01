__all__ = ["sync_table"]

# -- STANDARD LIBRARY IMPORTS
from os import environ
# -- CASSANDRA IMPORTS
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

# Setup CQL Schema Management
environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

# Setup Connection
connection.setup(["127.0.0.1"], default_keyspace="proximium")
