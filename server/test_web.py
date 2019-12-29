import pymysql.cursors
import tornado.ioloop
import tornado.web

class MysqlServer():
    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.user = kwargs.get('user')
        self.passwd = kwargs.get('passwd')
        self.db_name = kwargs.get('db')
        self.con = None

    def connect(self):
        self.con = pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.passwd,
                             db=self.db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    
    def insert(self, sql, *args, commit=False, many=False):
        assert self.con != None, 'fuck the connect has not been created...'
        affected = 0
        with self.con.cursor() as cursor:
            if many:
                affected = cursor.executemany(sql, args)
            else:
                affected = cursor.execute(sql, args)
        
        if commit:
            self.con.commit()
        return affected # how many rows affected

    def select(self, sql, *args, fetchall=False,nums=1):
        assert self.con != None, 'fuck the connection has not been made'
        with self.con.cursor() as cursor():
            cursor.execute(sql, args)
            if fetchall:
                return cursor.fetchall()
            else if nums <= 1:
                return cursor.fetchone()
            else:
                return cursor.fetchmany(size=nums)
        return {}

    def calLproc(self, procname, *args):
        pass # to do 
    
    def close(self):
        self.con.close() 


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

class QueryApiHandler(tornado.web.RequestHandler):
    def get(self):
         pass


def make_app():
    return tornado.web.Application([
	    (r"/", MainHandler), 
	])

if __name__ == "__main__":
    app = make_app()
    app.listen(3111)
    tornado.ioloop.IOLoop.current().start()
