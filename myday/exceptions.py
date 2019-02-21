class MyDayException(Exception):
    """All exceptions explicit raised should subclass MyDayException."""


class ProjectNotFound(MyDayException, ValueError):
    """The desired project does not exist."""
