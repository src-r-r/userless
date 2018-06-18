#!/usr/bin/env python3


def read_from(path, require=False, mode='r'):
    """ Read text from a file.

    :param path: Path to the file to read.

    :param require: If `False`, the method will fail silently and return
    `None`. Otherwise

    :param
    """
    import os
    if (not require) and (not os.path.exists(path)):
        return None
    with open(path, mode='r') as f:
        return f.read()


def write_to(path, content, require=False, create=True, mode='w+'):
    """ Write content to a path

    :param path: Path to the file.

    :param content: Text to write to the file.

    :param require: If set to `False`, this method will fail aislentl
    """
    import os
    d = os.path.dirname(path)
    if (not require) and not(os.path.exists(d)) and create:
        os.makedirs(d)
    with open(path, mode) as f:
        f.write(content)
    return True
