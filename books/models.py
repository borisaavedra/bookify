import uuid

class Books:

    def __init__(seft, name, author, year, publisher, topic, uid=None):
        seft.name = name
        seft.author = author
        seft.year = year
        seft.publisher = publisher
        seft.topic = topic
        seft.uid = uid or uuid.uuid4()

    def to_dict(seft):
        return vars(seft)

    @staticmethod
    def schema():
        return ["name", "author", "year", "publisher", "topic", "uid"]

    