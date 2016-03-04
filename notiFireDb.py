from json import load as json_load, dump as json_dump
from os import remove
from os.path import exists


class NotiFireDb(object):
    FILE = "1.json"  #TODO consider sqlite or at least file locking

    @classmethod
    def register(cls, name, address):
        file_exists = exists(cls.FILE)
        mode = "r+" if file_exists else "w"
        with open(cls.FILE, mode) as f:
            json_obj = json_load(f) if file_exists else {}
            json_obj[name] = address# <--- add `id` value.
            f.seek(0)        # <--- should reset file position to the beginning.
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


def unit_test():
    try:
        NotiFireDb.FILE = "unittest.json"
        t1 = "name1", "a1"
        NotiFireDb.register(*t1)
        NotiFireDb.register("name2", "a2")
        if NotiFireDb.get_address(t1[0]) != t1[1]:
            raise Exception("Can't get address")
        if NotiFireDb.get_name(t1[1]) != t1[0]:
            raise Exception("Can't get name")

        try:
            NotiFireDb.get_name("nop")
            raise ("Improper error handling: get_name")
        except:
            pass
        try:
            NotiFireDb.get_address("nop")
            raise ("Improper error handling: get_address")
        except:
            pass
    finally:
        if exists(NotiFireDb.FILE):
            remove(NotiFireDb.FILE)


if __name__ == "__main__":
    unit_test()
