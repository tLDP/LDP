insert(001,
    [Pas de fichier source],
    [Pas de fichier source pour ce document.])
insert(002,
    [Pas de fichier source principal],
    [Pas de fichier source principal.])
insert(003,
    [Plusieurs fichiers source principaux],
    [Plus d'un fichier source principal.])
insert(101,
    [Fichier introuvable],
    [Ce fichier n\'existe pas dans le cache du cvs de Lampadas.])
insert(102,
    [Fichier illisible],
    [Ce fichier existe, mais est illisible.])
insert(103,
    [Fichier protégé en écriture],
    [Ce fichier existe, mais est protégé en écriture.])
insert(104,
    [Format de fichier indéterminé],
    [Lampadas ne peut déterminer le format de ce fichier contenant ce document et ne donc pas le publier.])
insert(201,
    [Impossible de faire un miroir, fichier introuvable.],
    [Le système de miroir n\'a pas réussi à copier le fichier source car il est introuvable.])
insert(202,
    [Could not retrieve remote file.],
    [The mirroring system was unable to retrieve a remote file over HTTP or FTP.])
insert(301,
    [Cannot make because a source file is missing.],
    [The Make system tried to make the document, but a source file is missing.
    Th document will not be publishable until the problem is resolved.])
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
