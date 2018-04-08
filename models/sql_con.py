
class SQLConnect():

    def __init__(self, **kwargs):
        for item, value in kwargs.items():
            setattr(self, item, value)

    def make_conn_string(self):
        if self.conn_string:
            return self.conn_string
        else:
            return 'postgresql://%s:%s@%s:%s/%s' %(self.login, self.password, self.host, self.port, self.db_name)