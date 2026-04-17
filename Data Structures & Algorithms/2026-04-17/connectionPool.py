from cgi import test
from termios import VLNEXT
import uuid

class DBConnection:
   def __init__(self):
       self.id = uuid.uuid4().hex[:8]

   def query(self, q: str) -> str:
       return f"result({q})"

   def close(self):
       return "DBConnection closed"

class ConnectionPool:

    def __init__(self, maxConnections):
        self.max_connections = maxConnections
        self.available = []
        self.created_count = 0

        if self.max_connections <= 0:
            raise ValueError("Invalid max connections limit")

    def get_connection(self):
        '''
        Supplies dbConnections.
        '''

        if self.available:
            return PooledConnection(self, self.available.pop())
        elif self.created_count < self.max_connections:
            dbConnection = DBConnection()
            self.created_count += 1
            return PooledConnection(self, dbConnection)
        else:
            raise RuntimeError("Max connections limit reached.")

    def _return_connection(self, dbConnection):
        self.available.append(dbConnection)
        

class PooledConnection:

    def __init__(self, parent, dbConnection):
        self.parent = parent
        self.dbConnection = dbConnection
        self.is_closed = False

    def query(self, q):
        if self.is_closed:
            raise ValueError("Connection is closed.")
        
        return self.dbConnection.query(q)

    def close(self):
        if self.is_closed:
            return

        self.parent._return_connection(self.dbConnection)
        self.is_closed = True

def test_basic_operations():
    connection_pool = ConnectionPool(1)
    pooled_connection = connection_pool.get_connection()

    assert isinstance(connection_pool, PooledConnection)
    q = "query"
    assert pooled_connection.query(q) == f"result({q})"
    pooled_connection.close()

def test_pool_cannot_be_created_with_non_positive_max_num_connections():
    assert_raises(lambda: ConnectionPool(0), "ValueError")
    assert_raises(lambda: ConnectionPool(-1), "ValueError")

def test_connections_are_lazily_created():
    c = ConnectionPool(2)
    assert c.created_count == 0
    assert len(c.available) == 0

    p1 = c.get_connection()
    assert c.created_count == 1
    assert len(c.available) == 0
    
    p2 = c.get_connection()
    assert c.created_count == 2
    assert len(c.available) == 0

    p1.close()
    assert c.created_count == 2
    assert len(c.available) == 1

def test_more_than_max_num_connections_cannot_be_created():
    c = ConnectionPool(2)

    p1 = c.get_connection()
    p2 = c.get_connection()

    assert_raises(lamda: c.get_connection(), "RuntimeError")

def test_connections_are_reused_after_closing():
    c = ConnectionPool(1)

    p1 = c.get_connection()
    id1 = p1.dbConnection.id
    p1.close()

    p2 = c.get_connection()
    id2 = p2.dbConnection.id

    assert id1 == id2
    assert c.created_count == 1

def test_connection_close_is_idempotent():
    c = ConnectionPool(1)

    p = c.get_connection()
    p.close()
    p.close()

    assert len(c.available) == 1
    assert (c.created_count) == 1

def test_connection_cannot_be_queried_after_close():
    c = ConnectionPool(1)

    p = c.get_connection()
    p.close()

    assert_raises(lambda: p.query("A"), "ValueError")
