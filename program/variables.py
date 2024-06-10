import os


INTERNAL_PATH = ""
if os.path.isdir("_internal"):
    INTERNAL_PATH = "_internal/"

RESOURCE_PATH = INTERNAL_PATH+"resources/"