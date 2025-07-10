from flask_mysqldb import MySQL

def init_mysql(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Root12345'  # Put your MySQL password here if any
    app.config['MYSQL_DB'] = 'talentbridge'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    return MySQL(app)
