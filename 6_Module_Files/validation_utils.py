from datetime import datetime


def is_valid_date(inp_date: str) -> bool:
    """
    Check if the input date has a correct format DD/MM/YYYY
    """
    try:
        datetime.strptime(inp_date, '%d/%m/%Y')
        return True
    except:
        return False


def is_valid_degree(inp_degree: str) -> bool:
    """
    Check if the input value has an integer format
    """
    try:
        int(inp_degree)
        return True
    except:
        return False


def is_valid_pub_type(pub_type):
    """
    Check if the input is valid
    """
    if pub_type in ['1', '2', '3']:
        return True
    else:
        return False
