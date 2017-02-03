import pymysql.cursors

class DB:
    def __init__(self, dbHost, dbUser, dbPassword, dbName):
        self.conn = pymysql.connect(
            host = dbHost,
            user = dbUser,
            password = dbPassword,
            db = dbName,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )

    def runQuery(self, sql):
        try:
            with self.getCursor() as cursor:
                cursor.execute(sql)

            return cursor
        except Exception as e:
            raise Exception("Unable to execute query: {0}. Error: {1}".format(sql, str(e)))

    def save(self):
        # Commit changes
        self.getConnection().commit()

    def disconnect(self):
        self.getConnection().close()

    def getCursor(self):
        return self.conn.cursor()

    def getConnection(self):
        return self.conn
