from json import load as json_load, dump as json_dump
from os.path import exists
from logger import logger


class NotiFireDb(object):
    #TODO Maybe make configurable
    FILE = "1.json"  #TODO consider sqlite or at least file locking

    @classmethod
    def register(cls, name, address, port, old_name=None, **options):
        if exists(cls.FILE):
            with open(cls.FILE, "r+") as f:
                json_obj = json_load(f)
        else:
                json_obj = {}
        if name in json_obj:
            raise ValueError("Name already taken")

        if old_name in json_obj:
            logger.debug("Removing %s" % (old_name,))
            del json_obj[old_name]
        json_obj[name] = address, port, options
        with open(cls.FILE, "w") as f:
            json_dump(json_obj, f, indent=2, sort_keys=True)

    @classmethod
    def get_address(cls, name):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        return json_obj[name][:2]

    @classmethod
    def get_name(cls, address):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        for name, registered_address in json_obj.iteritems():
            if registered_address[0] == address:
                return name
        raise KeyError("Can't find address %s" % address)

    @classmethod
    def get_all_names(cls):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        return json_obj.keys()

    @classmethod
    def get_colour(cls, name):
        with open(cls.FILE) as f:
            json_obj = json_load(f)
        return json_obj[name][2]['colour']

    @classmethod
    def remove(cls, name):
        with open(cls.FILE, "r+") as f:
            json_obj = json_load(f)
        if name not in json_obj:
            logger.debug("No such name %s" % (name,))
            return False
        del json_obj[name]
        with open(cls.FILE, "w") as f:
            json_dump(json_obj, f, indent=2, sort_keys=True)
        return True


def unit_test():
    from os import remove
    try:
        NotiFireDb.FILE = 'unittest.json'
        t1 = 'name1', 'addr1', 0, 'blue'
        t2 = 'name2', 'addr2', 0
        NotiFireDb.register(*t1[:3], colour=t1[3])
        NotiFireDb.register(*t2)
        if tuple(NotiFireDb.get_address(t1[0])) != t1[1:3]:
            raise Exception("Can't get address")
        if NotiFireDb.get_name(t1[1]) != t1[0]:
            raise Exception("Can't get name")
        if set(NotiFireDb.get_all_names()) != {t1[0], t2[0]}:
            raise Exception("Can't get all name")
        if NotiFireDb.get_colour(t1[0]) != t1[3]:
            raise Exception("Can't get colour")

        NotiFireDb.remove(t1[0])
        try:
            NotiFireDb.get_name(t1[1])
            raise Exception('Improper error handling: get_name')
        except KeyError:
            pass
        try:
            NotiFireDb.get_address(t1[0])
            raise Exception('Improper error handling: get_address')
        except KeyError:
            pass
    finally:
        if exists(NotiFireDb.FILE):
            remove(NotiFireDb.FILE)
    logger.debug("Passed unit-tests")


if __name__ == "__main__":
    unit_test()
