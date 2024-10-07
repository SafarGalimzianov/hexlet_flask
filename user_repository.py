from psycopg2.extras import RealDictCursor

class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        '''
        Использование оператора with для создания курсора, который извлекает данные как словарь
        курсор - это объект, который представляет результат запроса к базе данных
        оператор with гарантирует, что курсор будет закрыт после выполнения блока кода даже если возникнет исключение
        что гарантирует корректное (без непредвиденных изменений данных) закрытие соединения с базой данных
        '''
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM safar')
            return cur.fetchall()
        
    def get_by_term(self, term=''):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM safar WHERE name ILIKE %s', (f'%{term}%',))
            return cur.fetchall()
            
    def find(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM safar WHERE id = %s', (id,))
            return cur.fetchone()
            
    def save(self, user):
        if 'id' not in user:
            id = self._create(user)
        else:
            id = self._update(user)
        return id
        
    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO safar (name, email) VALUES (%s, %s) RETURNING id', (user['name'], user['email']))
            user['id'] = cur.fetchone()[0]
        self.conn.commit()
        return user['id']
        
    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute('UPDATE safar SET name  = %s, email = %s RETURNING id', (user['name'], user['email']))
            user['id'] = cur.fetchone()[0]
        self.conn.commit()
        return user['id']
        
    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM safar WHERE id = %s', (id,))
        self.conn.commit()