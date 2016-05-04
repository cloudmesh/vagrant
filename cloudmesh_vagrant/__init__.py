from .vm.vm import vm
from .image.image import image
from cloudmesh_client.common.Shell import Shell

__version__ = "1.0"

def version(verbose=False):
    result = Shell.execute("vagrant", ["version"])
    if verbose:
        return result
    else:
        lines = result.split("\n")
        for line in lines:
            if "Installed Version:" in line:
                return line.replace("Installed Version:", "").strip()
        return None
