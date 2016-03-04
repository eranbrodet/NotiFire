from json import load as json_load, dump as json_dump
from os.path import exists


class NotiFireDb(object):
    FILE = "1.json"  #TODO consider sqlite or at least file locking

    @classmethod
    def register(cls, name, address):
        if exists(cls.FILE):
            with open(cls.FILE, "r+") as f:
                json_obj = json_load(f)
        else:
                json_obj = {}
        json_obj[name] = address
        with open(cls.FILE, "w") as f:
            json_dump(json_obj, f, indent=4, sort_keys=True)

    @classmethod
    def get_address(cls, name):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        return json_obj[name]

    @classmethod
    def get_name(cls, address):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        for name, redigstered_addres in json_obj.iteritems():
            if redigstered_addres == address:
                return name
        raise KeyError("Can't find address %s" % address)

    @classmethod
    def get_all_names(cls):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        return json_obj.keys()


def unit_test():
    from os import remove
    try:
        NotiFireDb.FILE = "unittest.json"
        t1 = "name1", "a1"
        t2 = "name2", "a2"
        NotiFireDb.register(*t1)
        NotiFireDb.register(*t2)
        if NotiFireDb.get_address(t1[0]) != t1[1]:
            raise Exception("Can't get address")
        if NotiFireDb.get_name(t1[1]) != t1[0]:
            raise Exception("Can't get name")
        if set(NotiFireDb.get_all_names()) != {t1[0], t2[0]}:
            raise Exception("Can't get all name")
        try:
            NotiFireDb.get_name("nop")
            raise Exception("Improper error handling: get_name")
        except:
            pass
        try:
            NotiFireDb.get_address("nop")
            raise Exception("Improper error handling: get_address")
        except KeyError:
            pass
    finally:
        if exists(NotiFireDb.FILE):
            remove(NotiFireDb.FILE)
        print "Passed unit-test"


if __name__ == "__main__":
    unit_test()
