import urllib
from functools import partial


class Sharable(object):

    read_permissions = [
        "read_data",
        "read_triggers",
    ]

    write_permissions = [
        "write_data",
        "write_triggers",
    ]

    manage_permissions = [
        "manage_triggers",
        "manage_sharing",
    ]

    all_permissions = (
        read_permissions +
        write_permissions +
        manage_permissions
    )

    def _share_path(self, email=None):
        if not email:
            return "%s/users" % self._path()
        return "%s/users/%s" % (self._path(), urllib.quote(email))

    def get_sharing(self):
        return self.wink._get(self._share_path())

    def share_with(self, email, permissions):
        permissions = set(permissions) & set(Sharing.all_permissions)
        data = dict(
            email=email,
            permissions=list(permissions),
        )
        return self.wink._post(self._share_path(), data)

    def unshare_with(self, email):
        return self.wink._delete(self._share_path(email))

def dataProperties(properties):
    """ Create properties on the decorated class that access self.data.
    
    This class decorator allows you to add properties to get/set values
    in data. Provide a list containing tuples containing the key used to
    store the value, Can you set the value, and data type.
    """
    def class_rebuilder(cls):
        class NewClass(cls):
            _settable_fields = []
            
        # Dynamicly create getter's and setters on the class.
        def _get_value(key, self):
            return self.data.get(key)

        def _set_value(key, dataType, self, value):
            if not isinstance(value, dataType):
                raise ValueError('Invalid data type. Expected %s.' % dataType.__name__)
            self.data[key] = value
            
        # Add all of the properties to the class.
        for key, settable, dataType in properties:
            # Create the getter
            args = [partial(_get_value, key)]
            if settable:
                # if aplicable, create the setter.
                args.append(partial(_set_value, key, dataType))
                NewClass._settable_fields.append(key)
            setattr(NewClass, key, property(*args))
        NewClass.__name__ = cls.__name__
        return NewClass
    return class_rebuilder
