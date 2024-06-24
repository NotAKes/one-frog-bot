from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from config import emotes

ua = UserAgent()
dayURL = ''


def parser(date, list_) - > str:
    global dayURL
    hours = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00']

    # форматирование ссылки
    if date <= 2:
        dayURL = list_[date]
    elif date >= 3:
        dayURL = list_[1] + f'{date}-day/'

    # определение юзер-агента и гет реквест
    headers = {'User-Agent': ua.random}
    req = requests.get(dayURL, headers=headers)

    # суп температуры
    soup_temp = BeautifulSoup(req.text, 'lxml')
    paragraph = soup_temp.find_all('#any name', class_='#any class')  # температуры

    # суп осадков
    soup_precip = BeautifulSoup(req.text, 'lxml')
    precipitation = soup_precip.find_all('#any name', class_='#any class', )  # виды осадков

    # форматирование полученной информации
    # Получить информацию можем в двух вариациях. Отделим их условием

    if paragraph[0].text[-1:-3:-1] == 'C°':  # Первая вариация
        # Из-за большого количества видов осадков, может возникнуть ошибка из-за неналичия этого вида осадков в emotes
        # Для избежания ошибки используем try
        try:
            # начинаем форматировать строки на вывод в генераторе. Всего строк 8
            return '\n'.join(
                [hours[i] + "  |  " +  # Время в часах и разделитель для украшения
                 paragraph[3 + i].text + '°C' + "   " +  # Количество градусов Цельсия и пробелы-разделители
                 precipitation[i]['data-text'] +  # Вид осадков
                 emotes[precipitation[i]['data-text']] +  # Эмоджи из словаря emotes если все виды осадков есть в emotes
                 "\n" + "-" * 40  # Украшение
                 for i in range(8)])  # цикл
        except KeyError:  # Если хотя бы один вид осадков не найден, то все виды будут выведены без эмоджи
            return '\n'.join(
                [hours[i] + "  |  " +
                 paragraph[3 + i].text + '°C' + "   " +
                 precipitation[i]['data-text'] + "\n" + "-" * 40
                 for i in range(8)])

    else:  # Вторая вариация
        try:
            return '\n'.join(
                [hours[i] + "  |  " +
                 paragraph[7 + i].text + '°C' + "   "
                 + precipitation[i]['data-text']
                 + emotes[precipitation[i]['data-text']] +
                 "\n" + "-" * 40
                 for i in range(8)])
        except KeyError:
            return '\n'.join(
                [hours[i] + "  |  " +
                 paragraph[7 + i].text + '°C' "   "
                 + precipitation[i]['data-text']
                 + "\n" + "-" * 40
                 for i in range(8)])
