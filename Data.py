class Data:

    everything = {}

    @classmethod
    def save_data(cls, name, rest):
        if type(name) == list:
            name, obj = name[0], cls(name[1], rest)
        else:
            obj = cls(rest)
        cls.everything[name] = obj
        cls.show(name)
    
    @classmethod
    def show(cls, name):
        print(" ", cls.everything[name])
    
    @classmethod
    def reassign(cls, where, what):
        cls.everything[where] = cls.everything[what]
        cls.show(where)
