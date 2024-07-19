import requests
from config import emotes
from lxml import html

dayURL = ''


def parser(date, list_):
    global dayURL
    hours = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00']

    # форматирование ссылки
    dayURL = 'url-pattern/{date}'

    # определение юзер-агента и гет реквест
    headers = {
        'User-Agent': '#ua'}
    req = requests.get(dayURL, headers=headers)

    tree = html.fromstring(req.content)
    temperatures = []
    signs = []

    # получение информации по xpath
    for i in range(1, 9):
        paragraph = tree.xpath(
            f"#xpath")
        temperatures.append(paragraph[0].get('#value'))

        precipitation = tree.xpath(f'#xpath')
        signs.append(precipitation[0].get("#value"))
    # форматирование полученной информации
    # Из-за большого количества видов осадков, может возникнуть ошибка из-за неналичия этого вида осадков в emotes
    # Для избежания ошибки используем try
    try:
        # начинаем форматировать строки на вывод в генераторе. Всего строк 8
        return '\n'.join(
            [hours[i] + "  |  " +  # Время в часах и разделитель для украшения
             temperatures[i] + '°C' + "   "  # Количество градусов Цельсия и пробелы-разделители
             + signs[i]  # Вид осадков
             + emotes[
                 signs[i]] +  # Эмоджи из словаря emotes если все виды осадков есть в нём
             "\n" + "-" * 40  # Украшение
             for i in range(8)])  # Цикл
    except KeyError:
        return '\n'.join(
            [hours[i] + "  |  " +
             temperatures[i] + '°C' "   "
             + signs[i]
             + "\n" + "-" * 40
             for i in range(8)])
