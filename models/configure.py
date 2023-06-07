class Mongo:
    def __init__(self, connect: str):
        self.connect = connect


class Conf:
    logLevel: str
    verbose: bool
    port: int

    # a default constructor, without any parameters
    def __init__(
        self,
        logLevel: str = "info",
        verbose: bool = False,
        port: int = 15000,
        db: dict = None,
    ):
        self.logLevel = logLevel
        self.verbose = verbose
        self.port = port
        if db:
            if db.get("mongo"):
                self.mongo = Mongo(db["mongo"]["connect"])

    # a class method that creates a Conf object from a dictionary
    @classmethod
    def from_dict(cls, conf_dict: dict = {}) -> "Conf":
        if not conf_dict:
            conf_dict = {
                "logLevel": "info",
                "verbose": False,
                "port": 15000,
                "db": None,
            }

        return cls(
            conf_dict.get("logLevel", "info"),
            conf_dict.get("verbose", False),
            conf_dict.get("port", 15000),
            conf_dict.get("db", None),
        )
