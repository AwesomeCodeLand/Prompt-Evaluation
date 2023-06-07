from models.configure import Conf
from stores.mongo import mongoInit
from stores.sqlite import sqliteInit
from log import output_log

def sqlInit(conf:Conf):
    # If the mongo in conf is not None, then use mongo. Otherwise, use sqlite.
    # output the detail of the conf
    output_log(f"conf: {conf}", level="info")
    if conf.mongo is not None:
        try:
            mongoInit(conf.mongo.connect, conf.mongo.db)
        except Exception as e:
            output_log(f"mongoInit error: {e}", level="error")
    else:
        try:
            sqliteInit()
        except Exception as e:
            output_log(f"sqliteInit error: {e}", level="error")

