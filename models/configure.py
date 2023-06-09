class Mongo:
    def __init__(self, connect: str, db:str):
        self.connect = connect
        self.db = db


class Conf:
    logLevel: str
    verbose: bool
    port: int
    mongo: Mongo

    # a default constructor, without any parameters
    def __init__(
        self,
        logLevel: str = "info",
        verbose: bool = False,
        port: int = 15000,
        db: dict = None,
        mongo: Mongo = None,
    ):
        self.logLevel = logLevel
        self.verbose = verbose
        self.port = port
        self.mongo = mongo
        if db:
            if db.get("mongo"):
                self.mongo = Mongo(connect=db["mongo"]["connect"], db=db["mongo"]["name"])

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
