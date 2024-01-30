import sqlite3
class User:

    userDict = {}

    def __init__(self,id, fname, lname, email):

        self.id = str(id)
        self.fname = fname
        self.lname = lname
        self.email = email

    def is_authenticated(self):
        if(self.id in User.userDict):
            return True
        return False


    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query1 = "SELECT * FROM users WHERE id = {}".format(int(user_id))
        result = cursor.execute(query1).fetchall()[0]
        print(result)
        #return User(result[4],result[1],result[2],result[])




