insert(001,
    [No source files],
    [No source files are listed for the document.])
insert(002,
    [No primary files],
    [No source file is designated as primary.])
insert(003,
    [Multiple primary files],
    [More than one file is designated as primary.])
insert(101,
    [File not found],
    [The source file does not exist in the Lampadas cvs cache.])
insert(102,
    [File not readable],
    [The file exists, but Lampadas cannot read it.])
insert(103,
    [File not writable],
    [The source file exists, but is not writable.])
insert(104,
    [Cannot determine file format],
    [Lampadas cannot determine what format this file is stored in, so it cannot be published.])
insert(201,
    [Could not mirror file, file not found.],
    [The mirroring system was unable to locate the source file for mirroring.])
insert(202,
    [Could not retrieve remote file.],
    [The mirroring system was unable to retrieve a remote file over HTTP or FTP.])
insert(301,
    [Cannot make because a source file is missing.],
    [The Make system tried to make the document, but a source file is missing.
    The document will not be publishable until the problem is resolved.])
insert(302,
    [Make command returned an error],
    [A command returned a nonzero (failure) exit status, and Make was aborted.])
insert(303,
    [Make command wrote to STDERR],
    [A command wrote output to STDERR.])
insert(304,
    [Make command wrote zero-length file.],
    [A command created an output file, but the length of that file is zero.])
insert(305,
    [Error replacing entities with UTF-8 characters.],
    [Tried to filter the source file through lampadas-filter, but it returned an error code.])
