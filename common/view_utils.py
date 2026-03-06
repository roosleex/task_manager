# Utilities for a django view



def is_trusted_user(user) -> bool:
    """
    Check if a current user is trusted
    user : 
        user
    """
    if user and user.is_staff==True and user.is_active==True and user.is_authenticated:
        return True
    return False



# def conv_str_to_datetime(d_str: str, format: str) -> datetime:
#     """
#     Convert from string format to datetime format
#     d_str : str
#         date in string format
#     format : str
#         format
#     """
#     result = ""

#     if d_str == "" or format == "":
#         return result
#     result = datetime.datetime.strptime(d_str, format)
#     return result










