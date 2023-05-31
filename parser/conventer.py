import requests
from bs4 import BeautifulSoup as bs


def convert_currency_xe(src, dst, amount):
    def get_digits(text):
        """
        Возвращает цифры и точки только из входного
        "текста" в виде числа с плавающей точкой.
        :param text: str текст с числами.
        :return: float сумма перевода
        """
        """Returns the digits and dots only from an input `text` as a float
        Args:
            text (str): Target text to parse
        """
        new_text = ""
        for c in text:
            if c.isdigit() or c == ".":
                new_text += c
        return float(new_text)

    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={src}&To={dst}"
    content = requests.get(url).content
    soup = bs(content, "html.parser")
    exchange_rate_html = soup.find_all("p")[2]

    return get_digits(exchange_rate_html.text)
