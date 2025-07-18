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
import aiohttp
import asyncio

def create_folder():
    done = True
    path = None
    while done:
        path = input()
        if '..' in path:
            print("Вы можете создать папку только в папке src/")
            continue
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0o770)
                done = False
            except: 
                print("Не удалось создать папку, попробуйте еще раз")
        elif not os.access(path, os.W_OK):
            print("Недостаточно прав")
        else:
            done = False
    return path

def collect_links():
    link = None
    urls = []
    done = True
    counter_links = 0
    while done:
        link = input().strip() 
        if link == '':
            done = False
        else:
            urls.append(link)
            counter_links += 1
            print(f"Добавлено ссылок: {counter_links}")
    return urls

async def download_one_image(session, urls, i, path, successes, failures):
    try:
        async with session.get(urls) as resp:
            content = await resp.read()
            file_path = os.path.join(path, f"img_{i+1}.jpg") 
            with open(file_path, 'wb') as f:
                f.write(get(u).content)
            successes.append(urls)
    except Exception as e:
            failures.append((urls, str(e)))

asyc def download_all_images(path, urls):
    successes = []
    failures = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, u in enumerate(urls):
            task = asyncio.create_task(download_one_image(session, urls, i, path, successes, failures))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return successes, failures

def main():
    # os.system('cls' if os.name == 'nt' else 'clear')
    path = create_folder()
    urls = collect_links()
    download_file(path, urls)

if __name__=="__main__":
    main()