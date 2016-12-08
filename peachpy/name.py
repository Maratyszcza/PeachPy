# This file is part of PeachPy package and is licensed under the Simplified BSD license.
#    See license.rst for the full text of the license.

import six


class Name:
    def __init__(self, name=None, prename=None):
        assert name is None or isinstance(name, str)
        assert prename is None or isinstance(prename, str)
        assert name is None or prename is None, \
            "Either name or prename, but not both, can be specified"
        self.name = name
        self.prename = prename

    def __str__(self):
        if self.name is not None:
            return self.name
        elif self.prename is not None:
            return "<" + self.prename + ">"
        else:
            return "<?>"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name) ^ id(self)

    def __eq__(self, other):
        return isinstance(other, Name) and (self is other or self.name == other.name)

    def __ne__(self, other):
        return not isinstance(other, Name) or (self is not other and self.name != other.name)

    @staticmethod
    def check_name(name):
        """Verifies that the name is appropriate for a symbol"""
        if not isinstance(name, str):
            raise TypeError("Invalid name %s: string required" % str(name))
        import re
        if not re.match("^[_a-zA-Z]\\w*$", name):
            raise ValueError("Invalid name: " + name)
        if name.startswith("__"):
            raise ValueError("Invalid name %s: names starting with __ are reserved for PeachPy purposes" % name)


class Namespace:
    def __init__(self, scope_name):
        assert scope_name is None or isinstance(scope_name, Name)
        # Name of the namespace.
        self.scope_name = scope_name
        # Map from name string to either Name or Namespace object
        self.names = dict()
        # Map from prename string to a set of Name and Namespace objects
        self.prenames = dict()

    def __str__(self):
        return str(self.scope_name)

    def __hash__(self):
        return hash(self.scope_name)

    def __eq__(self, other):
        return isinstance(other, Namespace) and self.scope_name == other.scope_name

    def __ne__(self, other):
        return not isinstance(other, Namespace) or self.scope_name != other.scope_name

    def add_scoped_name(self, scoped_name):
        assert isinstance(scoped_name, tuple)
        scope_name, subscoped_name = scoped_name[0], scoped_name[1:]
        assert isinstance(scope_name, Name)
        scope = scope_name
        if subscoped_name:
            scope = Namespace(scope_name)
            scope.add_scoped_name(subscoped_name)
        if scope_name.name:
            assert scope_name.prename is None
            if scope_name.name in self.names:
                if subscoped_name and isinstance(self.names[scope_name.name], Namespace):
                    self.names[scope_name.name].add_scoped_name(subscoped_name)
                else:
                    raise ValueError("Name %s already exists" % scope_name.name)
            else:
                self.names[scope_name.name] = scope
        else:
            assert scope_name.name is None
            self.prenames.setdefault(scope_name.prename, set())
            if subscoped_name:
                for subscope in iter(self.prenames[scope_name.prename]):
                    if isinstance(subscope, Namespace) and subscope.scope_name is scope_name:
                        subscope.add_scoped_name(subscoped_name)
                        return
            self.prenames[scope_name.prename].add(scope)

    def assign_names(self):
        # Step 1: assign names to symbols with prenames with no conflicts
        for prename in six.iterkeys(self.prenames):
            if prename is not None:
                if len(self.prenames[prename]) == 1 and prename not in self.names:
                    name_object = next(iter(self.prenames[prename]))
                    self.names[prename] = name_object
                    if isinstance(name_object, Namespace):
                        name_object = name_object.scope_name
                    name_object.name = prename

        # Step 2: assign names to symbols with conflicting prenames
        for prename, prename_objects in six.iteritems(self.prenames):
            if prename is not None:
                suffix = 0
                suffixed_name = prename + str(suffix)
                for name_object in iter(prename_objects):
                    # Check that the name wasn't already assigned at Step 1
                    if name_object.name is None:
                        # Generate a non-conflicting name by appending a suffix
                        while suffixed_name in self.names:
                            suffix += 1
                            suffixed_name = prename + str(suffix)
                        self.names[suffixed_name] = name_object
                        if isinstance(name_object, Namespace):
                            name_object = name_object.scope_name
                        name_object.name = suffixed_name

        # Step 3: assign names to symbols without prenames
        if None in self.prenames:
            unnamed_objects = self.prenames[None]
            suffix = 0
            suffixed_name = "__local" + str(suffix)
            for name_object in iter(unnamed_objects):
                # Generate a non-conflicting name by appending a suffix
                while suffixed_name in self.names:
                    suffix += 1
                    suffixed_name = "__local" + str(suffix)
                self.names[suffixed_name] = name_object
                if isinstance(name_object, Namespace):
                    name_object = name_object.scope_name
                name_object.name = suffixed_name
        pass

    @property
    def name(self):
        return self.scope_name.name

    @property
    def prename(self):
        return self.scope_name.prename
