class Data:

    everything = {}

    @classmethod
    def save_data(cls, name, rest):
        obj = cls(name, rest)
        cls.everything[name] = obj
        print(obj)
    
    @classmethod
    def show(cls, name):
        print(cls.everything[name])
    
    @classmethod
    def reassign(cls, where, what):
        cls.everything[where] = cls.everything[what]
        cls.show(where)
