import requests
from bs4 import BeautifulSoup as bs
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def read_json(file_name: str) -> dict:
    """
    Десериализация JSON файла.
    При ошибке чтения файла, вернёт пустой список, чтобы последующий цикл не отработал.
    :param file_name:
    :return:
    """
    try:
        with open(file_name, "r") as f:
            logging.info(f"Файл {file_name} успешно прочитан.")
            return json.load(f)
    except Exception as e:
        logging.error(f" Файл {file_name} или директория отсутствуют. \n {e}")
        return {"coordinates": []}


def save_json(to_json: dict) -> None:
    with open('temperature.json', 'w') as f:
        json.dump(to_json, f, indent=4, ensure_ascii=False, separators=(',', ': '))
        logging.info(f"Список записан в файл temperature.json.")


def main():
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
    parse_list = {"temp": []}
    coordinate_dict = read_json("coordinates.json")
    for elem in coordinate_dict["coordinates"]:
        rez = {}
        url = f'https://yandex.com.am/weather/maps/nowcast?via=mmapwb&lat={elem["latitude"]}&lon={elem["longitude"]}'
        respons = requests.get(url, headers=headers)
        if respons.status_code != 200:
            logging.warning(f"Код ответа {respons.status_code}. Страница не прочитана. \n {url}")
        txt = bs(respons.text, "lxml")
        rez["fact_location"] = txt.find('h2', 'weather-maps-fact__location').text
        rez["fact_title"] = txt.find('h1', 'weather-maps-fact__title').text
        tmp_t = txt.find('span', 'temp__value temp__value_with-unit').text
        rez["temp_sign"], rez["temp_value"] = ("", int(tmp_t)) if tmp_t[0].isdigit() else (tmp_t[0], int(tmp_t[1:]))

        try:
            temp_weather = txt.find('div', 'weather-maps-fact__nowcast-alert').text
            rez["temp_weather"] = " ".join(temp_weather.split())
        except Exception as e:
            rez["temp_weather"] = "--"
            logging.warning(f"Отсутствует значение у ключа rez['temp_weather']. \n {e}\n{url}")
        parse_list["temp"].append(rez)
    logging.info(f"Список из {len(parse_list['temp'])} элементов для записи в файл temperature.json подготовлен.")
    save_json(parse_list)


if __name__ == '__main__':
    main()
