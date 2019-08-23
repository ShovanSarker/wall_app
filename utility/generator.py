import random
import uuid


def random4():
    """
    This is to generate 4 digit code in string
    :return: random 4 digit string
    """
    return str(random.randrange(1000, 9999))


def uuid36():
    """
    This is to generate 36 char UUID
    :return: UUID as string
    """
    return str(uuid.uuid4())
