from __future__ import print_function

from docopt import docopt
import cloudmesh_vagrant as vagrant
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.Shell import Shell
import sys
import os
from cloudmesh_vagrant.version import __version__
# pprint (vagrant.vm.list())
# vagrant.vm.execute("w2", "uname")
# pprint (vagrant.image.list())

def defaults():
    """
    default values
    :return: a number of default values for memory, image, and script
    :rtype: dotdict
    """
    d = dotdict()
    d.memory = 1024
    # d.image = "ubuntu/xenial64"
    d.image = "ubuntu/trusty64"
    d.port = 8080
    d.script = None
    return d



def _convert(lst, id="name"):
    d = {}
    for entry in lst:
        d[entry[id]] = entry
    return d


def _LIST_PRINT(l, output, order=None):
    if output in ["yaml", "dict", "json"]:
        l = _convert(l)

    result = Printer.write(l,
                           order=order,
                           output=output)

    if output in ["table", "yaml", "json", "csv"]:
        print(result)
    else:
        pprint(result)


def main():
    """
    ::

        Usage:
          cm-vbox version [--format=FORMAT]
          cm-vbox image list [--format=FORMAT]
          cm-vbox image find NAME
          cm-vbox image add NAME
          cm-vbox vm list [--format=FORMAT] [-v]
          cm-vbox vm delete NAME
          cm-vbox create NAME ([--memory=MEMORY]
                               [--image=IMAGE]
                               [--script=SCRIPT] | list)
          cm-vbox vm boot NAME ([--memory=MEMORY]
                                [--image=IMAGE]
                                [--port=PORT]
                                [--script=SCRIPT] | list)
          cm-vbox vm ssh NAME [-e COMMAND]
          cm-vbox -h | --help | --version
        """
    arg = dotdict(docopt(main.__doc__))
    arg.format = arg["--format"] or "table"
    arg.verbose = arg["-v"]

    if arg.version:
        versions = {
            "vagrant": {
               "attribute": "Vagrant Version",
                "version": vagrant.version(),
            },
            "cloudmesh-vbox": {
                "attribute":"cloudmesh vbox Version",
                "version": __version__
            }
        }
        _LIST_PRINT(versions, arg.format)

    elif arg.image and arg.list:
        l = vagrant.image.list(verbose=arg.verbose)
        _LIST_PRINT(l, arg.format, order=["name", "provider", "date"])

    elif arg.image and arg.add:
        l = vagrant.image.add(arg.NAME)
        print(l)

    elif arg.image and arg.find:
        l = vagrant.image.find(arg.NAME)
        print(l)

    elif arg.vm and arg.list:
        l = vagrant.vm.list()
        _LIST_PRINT(l,
                   arg.format,
                   order=["name", "state", "id", "provider", "directory"])

    elif arg.create and arg.list:

        result = Shell.cat("{NAME}/Vagrantfile".format(**arg))
        print (result)

    elif arg.create:

        d = defaults()

        arg.memory = arg["--memory"] or d.memory
        arg.image = arg["--image"] or d.image
        arg.script = arg["--script"] or d.script

        vagrant.vm.create(
            name=arg.NAME,
            memory=arg.memory,
            image=arg.image,
            script=arg.script)

    elif arg.boot:

        d = defaults()

        arg.memory = arg["--memory"] or d.memory
        arg.image = arg["--image"] or d.image
        arg.script = arg["--script"] or d.script
        arg.port = arg["--port"] or d.port

        vagrant.vm.boot(
            name=arg.NAME,
            memory=arg.memory,
            image=arg.image,
            script=arg.script,
            port=arg.port)

    elif arg.delete:

        result = vagrant.vm.delete(name=arg.NAME)
        print(result)

    elif arg.ssh:

        if arg.COMMAND is None:
            os.system("cd {NAME}; vagrant ssh {NAME}".format(**arg))
        else:
            result = vagrant.vm.execute(arg.NAME, arg.COMMAND)
            if result is not None:
                lines = result.splitlines()[:-1]
                for line in lines:
                    print (line)

    else:

        print ("use help")

if __name__ == '__main__':
    main(sys.arg)
