def check_params(param_dict, keys):
    """
    This is to check if all the requires parameters are in the param_dict

    :param param_dict: list of all parameters
    :param keys: the keys to confirm present
    :return : True if all the required keys in param_dict, False otherwise
    """
    for key in keys:
        if key not in param_dict.keys():
            return False
    return True
