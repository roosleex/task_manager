# Utilities for numbers

from decimal import Decimal, InvalidOperation



def conv_ton_to_kg(tons: float, roundNum: int = 0) -> float:
    """
    Convert tons to kilograms
    tons : float
        tons
    roundNum : int
        number of digits after the decimal point
    """
    result = round(tons * 1000, roundNum)
    return result



def get_fraction_digits_quantity(value):
    """
    Get quantity of fraction digits in a value
    value:
        value
    """
    try:
        d = Decimal(str(value))  # keep exact representation
        return -d.as_tuple().exponent if d.as_tuple().exponent < 0 else 0
    except (InvalidOperation, ValueError, TypeError):
        return 0
    


def num_to_string(num) -> str:
    """
    Convert number to string
    num: number
    """
    return str(num).replace(".", ",")



def money_to_string(num) -> str:
    """
    Convert money number to string
    num: number
    """
    return str(f"{num:.2f}".replace(".", ","))



def ukrainian_number_to_text(n, gender="m") -> str:
    """
    Convert integer n to Ukrainian text.
    gender: "m" (masculine) or "f" (feminine, e.g., для 'гривня')
    Works for 0-999
    """
    try:
        n = int(n)
    except (ValueError, TypeError):
        return ""

    if n < 0 or n > 999:
        return ""

    units = {
        "m": ["", "один", "два", "три", "чотири", "п'ять", "шість", "сім", "вісім", "дев'ять"],
        "f": ["", "одна", "дві", "три", "чотири", "п'ять", "шість", "сім", "вісім", "дев'ять"]
    }
    teens = ["десять", "одинадцять", "дванадцять", "тринадцять", "чотирнадцять",
             "п'ятнадцять", "шістнадцять", "сімнадцять", "вісімнадцять", "дев'ятнадцять"]
    tens = ["", "", "двадцять", "тридцять", "сорок", "п'ятдесят",
            "шістдесят", "сімдесят", "вісімдесят", "дев'яносто"]
    hundreds = ["", "сто", "двісті", "триста", "чотириста", "п'ятсот",
                "шістсот", "сімсот", "вісімсот", "дев'ятсот"]

    if n == 0:
        return "нуль"

    words = []

    h = n // 100
    t = (n % 100) // 10
    u = n % 10

    if h > 0:
        words.append(hundreds[h])

    if t == 1:
        words.append(teens[u])
    else:
        if t > 1:
            words.append(tens[t])
        if u > 0:
            words.append(units[gender][u])

    return " ".join(words)


def get_ukrainian_number_form(n, forms):
    """
    Return correct form based on number:
    forms = ["singular", "few", "many"]
    """
    n = abs(n) % 100
    if 11 <= n <= 19:
        return forms[2]
    n = n % 10
    if n == 1:
        return forms[0]
    if 2 <= n <= 4:
        return forms[1]
    return forms[2]


def money_to_ukr_text(amount) -> str:
    """
    Convert float amount to Ukrainian text with correct word forms.
    Example: 105.78 -> "сто п'ять гривень 78 копійок"
    """
    
    try:
        # amount is OK
        amount = float(amount)
    except (ValueError, TypeError):
        return ""


    hryvnias = int(amount)
    kopecks = round((amount - hryvnias) * 100)

    result = []

    # Millions
    millions = hryvnias // 1_000_000
    if millions > 0:
        result.append(ukrainian_number_to_text(millions))
        result.append(get_ukrainian_number_form(millions, ["мільйон", "мільйони", "мільйонів"]))
    hryvnias %= 1_000_000

    # Thousands
    thousands = hryvnias // 1000
    if thousands > 0:
        result.append(ukrainian_number_to_text(thousands, gender="f"))
        result.append(get_ukrainian_number_form(thousands, ["тисяча", "тисячі", "тисяч"]))
    hryvnias %= 1000

    # Hundreds/tens/units - use **feminine** for гривня
    if hryvnias > 0:
        result.append(ukrainian_number_to_text(hryvnias, gender="f"))
    result.append(get_ukrainian_number_form(hryvnias, ["гривня", "гривні", "гривень"]))
    
    if hryvnias == 0 and (len(result) == 1):
        result[0] = f"нуль {result[0]}"

    # Kopecks
    kopecks_text = f"{kopecks:02d}"
    result.append(f"{kopecks_text} {get_ukrainian_number_form(kopecks, ['копійка', 'копійки', 'копійок'])}")

    return " ".join(result)












