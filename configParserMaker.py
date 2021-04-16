import configparser,os

class maker:
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        if os.path.exists('config.ini')!= True:
            self.makeConf()

    def makeConf(self):
        config = configparser.ConfigParser()
        config['default'] = {
        "host" : self.host,
        "username" : self.user,
        "password" : self.password,
        "database" : self.database
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
