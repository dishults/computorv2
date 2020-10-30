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