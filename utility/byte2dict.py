import json


def convert(byte):
    """
    Converts response in byte firstly to string then converts the json string to dictionary
    :param byte: byte string
    :return: dictionary object
    """
    return json.loads(byte.decode("utf-8"))

