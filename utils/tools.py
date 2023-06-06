def changeLogLevel(logLevel: str) -> int:
    """
    Change the str log level to int.
    debug:0
    info:1
    warning:2
    error:3
    """
    if logLevel == "debug":
        return 0
    elif logLevel == "info":
        return 1
    elif logLevel == "warning":
        return 2
    else:
        return 3
