"""
This package provides a querying interface to the back end database.

Every table in the database has a corresponding data manager class here
that handles the details of querying, inserting, saving, loading and
deleting data for that table. Of course, most of these classes don't
really implement anything directly, because almost all normal operations
can be handled through the DataManager superclass.

There is no caching on this data, but a cache is planned.

To use these classes, instantiate a single instance of the DataManagers()
collection, which will automatically contain a reference to one of each
type of data manager. Before using it, assign the data managers with the
classes it should use to instantiate objects by calling set_object_classes()
and passing it in the name of the package which contains them. To use the
base persistence classes, call se_object_classes(persistence).
"""
