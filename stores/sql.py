from models.configure import Conf
from stores.mongo import mongoInit
from stores.sqlite import sqliteInit
from log import output_log
from models.sql import SqlBaseModel
from models.mongo import MongoModel
from models.sqlite import SqliteModel


def sqlInit(conf: Conf) -> SqlBaseModel:
    # If the mongo in conf is not None, then use mongo. Otherwise, use sqlite.
    # output the detail of the conf
    try:
        output_log(f"conf: {conf}", level="info")
        if conf.mongo is not None:
            return MongoModel(conf)

        else:
            return SqliteModel(conf)
    except Exception as e:
        raise e
