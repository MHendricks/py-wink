from interfaces import dataProperties

cls_properties = [
#    ('automation_mode', False),
    ('group_id', False, str),
    ('icon_id', True, int),
    ('members', True, dict),
    ('name', True, str),
    ('order', True, int),
#    ('reading_aggregation', False, dict),
]


@dataProperties(cls_properties)
class Group(object):
    """ Control groups.
        - get
        - update
        - delete
        
        Example:
            g = wink.init().group_list()[0]
            
            # Turn on/off power
            g.activate(dict(desired_state=dict(powered=True)))
            # Dim lights: For my group containing two lights, I had to specify powered for brightness to work.
            g.activate(dict(desired_state=dict(brightness=0.25, powered=True)))
            
            # re-name the group
            g.name = 'New Name'
            # Commit changes
            g.commit()
    """

    def __init__(self, wink, data):
        self.wink = wink
        # Store a copy of the original data
        self._old_data = data.copy()
        self.data = data
    
    def _path(self):
        return "/groups/%s" % (self.group_id)

    def activate(self, data):
        return self.wink._post('%s/activate' % self._path(), data)

    def commit(self):
        """ Update group with any changed properties.
        """
        output = {}
        for key in self._old_data:
            # Only update fields that are settable
            if key in self._settable_fields:
                # and that have changed
                if self.data[key] != self._old_data[key]:
                    output[key] = self.data[key]
        if output:
            return self.update(output)
        return {}

    def delete(self):
        return self.wink._delete(self._path())

    def get(self):
        return self.wink._get(self._path())

    def update(self, data):
        return self.wink._put(self._path(), data)

    def revert(self):
        """
        If you break anything, run this to revert the device
        configuration to the original value from when the object
        was instantiated.
        """
        self.data = self._old_data.copy()
