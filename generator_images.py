import base64
import json
import os
import time
import Api_keys             #Для запуска создайте свой файл с ключом к fusionbrain.io
import requests


class Text2ImageAPI:

    def __init__(self, url):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {Api_keys.api_key}',
            'X-Secret': f'Secret {Api_keys.secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        print(response.json())
        print(self.URL + 'key/api/v1/models')
        data = response.json()
        return data[0]['id']

    def generate(self, name, model, images=1, width=1024, height=1024):
        prompt = name + "Изображай сам предмет, располагай его по середине"
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, name, folder, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()

            if data['status'] == 'DONE':
                image_data = base64.b64decode(data['images'][0])
                f = "data"
                out = open(os.path.join(folder, f"{name}.png"), "wb")
                out.write(image_data)
                out.close()
                return 0

            attempts -= 1
            time.sleep(delay)

eating = ['Абрикос', 'Авокадо', 'Ананас', 'Апельсин', 'Арахис', 'Арбуз', 'Айва', 'Бананы','Брусника', 'Ваниль', 'Виноград', 'Вишня', 'Гранат', 'Грецкий орех', 'Гречка', 'Грибы', 'Груша', 'Дыня', 'Ежевика', 'Земляника', 'Инжир', 'Кабачки', 'Кальмар', 'Картофель', 'Кедровый орех', 'Кешью', 'Киви', 'Клубника', 'Клюква', 'Красная смородина', 'Кукуруза', 'Лайм', 'Лимон', 'Малина', 'Манго', 'Мандарины', 'Маракуйя', 'Маслины', 'Мёд', 'Морковь', 'Овсянка', 'Огурец', 'Оливки', 'Петрушка', 'Помидоры', 'Пшеница', 'Свёкла', 'Тыква', 'Фасоль', 'Хурма', 'Черешня', 'Черника', 'Чеснок', 'Чёрная смородина', 'Шелковица', 'Шиповник', 'Шоколад горький (чёрный)', 'Шпинат', 'Щавель', 'Эстрагон', 'Юзу', 'Яблоки', 'Яйца куриные', 'Ячневая крупа']

not_eating = ["Тарелка", "Ложка", "Стол", "Коробка", "Шкаф", "Камин", "Подушка", "Кровать", "Ванна", "Дом", "Машина", "Трактор", "Телефон", "Люстра", "Велосипед", "Коньки", "Лыжи"]
for i in eating:
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/')
    model_id = api.get_model()
    uuid = api.generate(i, model_id)
    images = api.check_generation(uuid, i, "eating")
    print(images)

for i in not_eating:
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/')
    model_id = api.get_model()
    uuid = api.generate(i, model_id)
    images = api.check_generation(uuid, i, "not_eating")
    print(images)