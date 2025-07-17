# Необходимо решить с задачу с применением мультипарадигмального подхода.
# Для написания асинхронного обработчика ссылок используй библиотеку `asyncio`.
# Сам процесс скачивания изображения можно реализовать при помощи библиотеки `requests`, в которой функция 
# `get` позволяет получить изображение с сервера по ссылке. Полученный ответ необходимо записать в файл по байтам.

# ```python
# from requests import get

# with open('test.jpg', 'wb') as f:
#     f.write(get('https://images2.pics4learning.com/catalog/s/swamp_15.jpg').content)

# Дополнительно потребуется обработать ошибки, которые могут возникнуть во время выполнения запроса. Для этого следует проверить `status_code`
# у объекта, который возвращается функцией `get`. Проверь, указан корректный путь или нет, можно, попытавшись сохранить туда что-либо.
# Исключение `PermissionError` вызывается в случае, если нет доступа по указанному пути.
from requests import get
import os
import sys

def create_folder():
    done = True
    while done:
        path = input()
        if '..' in path:
            print("Вы можете создать папку только в папке src/")
            continue
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0o770)
                return path
            except: 
                print("Не удалось создать папку, попробуйте еще раз")
        elif not os.access(path, os.W_OK):
            print("Недостаточно прав")
        else:
            done = False
    
def download_file(path):
    file_path = os.path.join(path, 'test.jpg')
    try:
        while True:
            link = input()
            if link 
            with open(file_path, 'wb') as f:
                f.write(get(link).content)
    except:
        link = '\n'

def main():
    # os.system('cls' if os.name == 'nt' else 'clear')
    path = create_folder()
    download_file(path)

if __name__=="__main__":
    main()