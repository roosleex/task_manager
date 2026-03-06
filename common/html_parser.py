from bs4 import BeautifulSoup



def get_select_selected_value(html: str, select_id: str) -> str:
    """
    Get selected value of a select element
    html: str
        html markup
    select_id: str
        id attribute of a select element
    """
    res = ""
    if not html or not select_id:
        return res
    soup = BeautifulSoup(html, "html.parser")
    select = soup.find(id=select_id)
    if not select:
        return res
    # print(f"select = {select}")
    select = str(select)
    soup2 = BeautifulSoup(select, "html.parser")
    option = soup2.find('option', selected=True)
    if not option:
        return res
    res = option['value']
    return res