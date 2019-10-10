class task():
    def __init__(self, name, about, date, priority, user):
        self.__name = name
        self.__about = about
        self.__date = date
        self.__priority = priority
        self.__user = user

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def about(self):
        return self.__about

    @about.setter
    def about(self, about):
        self.__about = about

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        self.__priority = priority
    
    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user