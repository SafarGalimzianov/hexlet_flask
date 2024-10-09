from psycopg2.extras import RealDictCursor

class UserRepository:
    def __init__(self, conn, table_name='users'):
        self.conn = conn
        self.table_name = table_name
        self._validate_table_name()
        with self.conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))')

    def _validate_table_name(self):
        if not self.table_name.isidentifier():
            raise ValueError('Invalid table name')

    def get_content(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f'SELECT * FROM {self.table_name}')
            return cur.fetchall()
        
    def get_by_term(self, term=''):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f'SELECT * FROM {self.table_name} WHERE name ILIKE %s', (f'%{term}%',))
            return cur.fetchall()
            
    def find(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f'SELECT * FROM {self.table_name} WHERE id = %s', (id,))
            return cur.fetchone()
            
    def save(self, user):
        if 'id' not in user:
            id = self._create(user)
        else:
            id = self._update(user)
        return id
        
    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(f'INSERT INTO {self.table_name} (name, email) VALUES (%s, %s) RETURNING id', (user['name'], user['email']))
            user['id'] = cur.fetchone()[0]
        self.conn.commit()
        return user['id']
        
    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(f'UPDATE {self.table_name} SET name = %s, email = %s WHERE id = %s RETURNING id', (user['name'], user['email'], user['id']))
            user['id'] = cur.fetchone()[0]
        self.conn.commit()
        return user['id']
        
    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute(f'DELETE FROM {self.table_name} WHERE id = %s', (id,))
        self.conn.commit()