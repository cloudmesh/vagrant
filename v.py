import cloudmesh_vagrant as vagrant
from pprint import pprint

#pprint (vagrant.vm.list())

# vagrant.vm.execute("w2", "uname")

#pprint (vagrant.image.list())
        
def convert(lst, id="name"):
    d = {}
    for entry in lst:
        d[entry[id]] = entry
    return d

#pprint (convert(vagrant.vm.list()))

#pprint (convert(vagrant.image.list()))

# vms = convert(vagrant.vm.list())

#vagrant.vm.execute("w2", "uname")


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



print (vagrant.version())

'''
vagrant.vm.boot(
    name="w2",
    memory=1024,
    image="ubuntu/trusty64",
    script="""
       sudo apt-get update
    """)
'''
