import json
from peewee import SqliteDatabase, MySQLDatabase

config = None
db = None

def load_config() -> None:
    global config, db
    with open("./config.json") as f:
        conf = json.load(f)
        database = None

        if not conf.get('server_secret') or len(conf.get('server_secret')) < 36:
            raise ValueError("load_config(): server_secret empty or less then 36 char")
        if not conf.get('salt') or len(conf.get('salt')) < 16:
            raise ValueError("load_config(): salt empty or less then 16 char")

        conf_db = conf.get('database')
        if not isinstance(conf_db, dict) or not conf_db.get('type'):
            raise ValueError("load_config(): invalid database config")

        if conf_db['type'] == 'sqlite':
            if not conf_db.get('file'):
                raise ValueError("load_condig(): 'file' is needed for sqlite db condig")
            database = SqliteDatabase(conf_db['file'])
            database.connect()
            database.pragma('foreign_keys', 1, permanent=True)
        elif conf_db['type'] == 'mysql':
            for x in ('host', 'dbname', 'user', 'password'):
                if not conf_db.get(x):
                    raise ValueError("load_condig(): '%s' is needed for MySQL db condig" % x)
            database = MySQLDatabase(
                conf_db['dbname'], host=conf_db['host'],
                user=conf_db['user'], passwd=conf_db['password'])
            database.connect()
        else:
            raise ValueError("load_condig(): unsupported database type '%s'" % conf_db['type'])

    # if no any error, apply to global var
    config = conf
    db = database

    # init database if not
    if not db.get_tables():
        from model import Class, User, Grade, Subject, Permission
        database.create_tables([Class, User, Grade, Subject, Permission])

        # Create admin user
        from random import randint
        from user import _hash_password
        from model import UserState
        email = "admin@cahcps-system.local"
        password = "guess_this"
        # password = hex(randint(1 << 60, (1 << 64) - 1))[2:]
        User.create(email=email, password=_hash_password(password), name="SYSADMIN", state=UserState.sysadmin)
        print("===========================================")
        print("           SysAdmin user created           ")
        print()
        print("Email:   ", email)
        print("Password:", password)
        print("===========================================")
