import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name        
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        '''
        CURSOR.execute(sql)
    
    @classmethod
    def drop_table(cls):
        sql = '''
            DROP TABLE IF EXISTS dogs
        '''
        CURSOR.execute(sql)
    
    def save(self):
        if self.id is None:
            sql = '''
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            '''
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            sql = '''
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            '''
            CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
    
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = '''
            SELECT *
            FROM dogs
        '''
        all_dogs = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all_dogs]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = '''
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        '''
        dog_row = CURSOR.execute(sql, (name,)).fetchone()
        if dog_row:
            return cls.new_from_db(dog_row)
        else:
            return None
    
    @classmethod
    def find_by_id(cls, dog_id):
        sql = '''
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        '''
        dog_row = CURSOR.execute(sql, (dog_id,)).fetchone()
        if dog_row:
            return cls.new_from_db(dog_row)
        else:
            return None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)
    
    def update(self):
        self.save()
        updated_dog = Dog.find_by_id(self.id)
        if updated_dog and updated_dog.name == self.name:
            return True
        else:
            return False


