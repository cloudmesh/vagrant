"""Usage:
  cm vbox version
  cm vbox image list [--format=FORMAT]
  cm vbox vm list [--format=FORMAT]
  cm vbox create NAME ([--memory=MEMORY] [--image=IMAGE] [--script=SCRIPT] | list)

  cm -h | --help | --version
"""
from docopt import docopt
import cloudmesh_vagrant as vagrant
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.Shell import Shell


# pprint (vagrant.vm.list())
# vagrant.vm.execute("w2", "uname")
# pprint (vagrant.image.list())

defaults = dotdict()
defaults.memory = 1024
defaults.image =  "ubuntu/trusty64"
defaults.script =  None


def convert(lst, id="name"):
    d = {}
    for entry in lst:
        d[entry[id]] = entry
    return d

# pprint (convert(vagrant.vm.list()))
# pprint (convert(vagrant.image.list()))
# vms = convert(vagrant.vm.list())
# vagrant.vm.execute("w2", "uname")

'''
f = vagrant.vm.vagrantfile(
    name="w2",
    memory=1024,
    image="ubuntu/trusty64",
    script="""
       sudo apt-get update
    """)

# print (f)

vagrant.vm.create(
    name="w2",
    memory=1024,
    image="ubuntu/trusty64",
    script="""
       sudo apt-get update
    """)


'''
# print (vagrant.version())

'''
vagrant.vm.boot(
    name="w2",
    memory=1024,
    image="ubuntu/trusty64",
    script="""
       sudo apt-get update
    """)
'''

def LIST_PRINT(l, output, order=None):
    if arg.format in ["yaml", "dict", "json"]:
        l = convert(l)

    result = Printer.write(l,
                           order=order,
                           output=arg.format)

    if output in ["table", "yaml", "json", "csv"]:
        print(result)
    else:
        pprint(result)


if __name__ == '__main__':

    arg = dotdict(docopt(__doc__, version='0.1'))
    arg.format = arg["--format"] or "table"


    if arg.version:
        print(vagrant.version())
    elif arg.image and arg.list:
        l = vagrant.image.list()
        LIST_PRINT(l, arg.format, order=["name", "provider", "date"])

    elif arg.vm and arg.list:
        l = vagrant.vm.list()
        LIST_PRINT(l,
                   arg.format,
                   order=["name", "state", "id", "provider", "directory"])

    elif arg.create and arg.list:

        result = Shell.cat("{NAME}/Vagrantfile".format(**arg))
        print (result)

    elif arg.create:

        arg.memory = arg["--memory"] or defaults.memory
        arg.image = arg["--image"] or defaults.iamge
        arg.script = arg["--script"] or defaults.script

        vagrant.vm.create(
            name=arg.NAME,
            memory=arg.memory,
            image=arg.image,
            provision=arg.script)
