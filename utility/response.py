import json


class RequestResponse:
    """
    This is the response factory. All the responses are created here
    """
    response = {}

    def __init__(self):
        """
        Empty response
        """
        self.response['status'] = 0
        self.response['message'] = ''
        self.response['data'] = None

    def set_status(self, status):
        """
        Set he status of the response
        :param status: status of the response
        :return:
        """
        self.response['status'] = status

    def set_message(self, message):
        """
        Adds message in the response
        :param message: message of the response
        :return:
        """
        self.response['message'] = message

    def set_data(self, data):
        """
        Adds data in the message
        :param data:
        :return:
        """
        self.response['data'] = data

    def respond(self):
        """
        Converts response object into JSON
        :return: the complete message in JSON as string
        """
        return dict(self.response)
