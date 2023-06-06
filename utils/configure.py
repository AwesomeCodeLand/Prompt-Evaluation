import toml
from models.configure import Conf
from pprint import pprint

conf = Conf()


def loadConfigure(path: str = "config.toml") -> Conf:
    """
    Configure the server with a toml file.
    """
    with open(path, "r") as f:
        config = toml.load(f)

    conf = Conf(**config)

    # pprint(vars(conf))
    setConfigPath(conf)
    return conf


def getConfigPath() -> Conf:
    """
    Get the configure path from environment variables.
    """
    # pprint(vars(conf))
    return conf


def setConfigPath(c: Conf):
    """
    Set the configure path from environment variables.
    """
    global conf
    conf = c
    return
