class Data:

    everything = {}

    @classmethod
    def save_data(cls, name, rest):
        if type(name) == list:
            name, obj = name[0], cls(name[1], rest)
        else:
            obj = cls(rest)
        cls.everything[name] = obj
        return cls.show(name)
    
    @classmethod
    def show(cls, name):
        return cls.everything[name]
    
    @classmethod
    def reassign(cls, where, what):
        cls.everything[where] = cls.everything[what]
        return cls.show(where)

    @classmethod
    def calculate(cls, func, var):
        obj = cls.everything[func]
        res = obj.calculate_with_variable(var, obj.expression[:])
        return res