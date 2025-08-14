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
import os
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
                os.makedirs(path, mode=0o770)
                if os.path.exists(path):
                    done = False
                else:
                    print("Не удалось создать папку, попробуйте еще раз")
        elif not os.access(path, os.W_OK):
            print("Недостаточно прав")
        else:
            done = False
    return path

async def download_one_image(session, u, i, path, successes, failures):
    done = True
    content = None
    resp = None
    file_path = os.path.join(path, f"img_{i+1}.jpg") 
    
    try:
        resp =  await session.get(u) #  асинхронный HTTP‑запрос к адресу файл + статус ответа
    except aiohttp.ClientError:
        failures.append((u, "Ошибка скачивания"))
        done = False
        resp = None

    if done and resp is not None and resp.status != 200 :
        failures.append((u, f"HTTP {resp.status}"))
        done = False

    if done and resp is not None:
        content = await resp.read()
        content_type = resp.headers.get("Content-Type", "")
        if not content or not content_type.startswith("image/"): 
            failures.append((u, "Нет данных для записи"))
            done = False

    if done and content is not None:
        f = open(file_path, 'wb')
        written = f.write(content)
        f.close()
        if written == 0:
            failures.append((u, "Не удалось записать файл"))
            done = False

    if done:
        successes.append(u)
    
    print(resp)

async def collect_links(session, path, successes, failures):
    link = None
    tasks = []
    done = True
    i = 0
    counter_links = 0
    
    while done:
        link = await asyncio.to_thread(input)
        if link == '':
            done = False
        else:
            urls.append(link)
            async with aiohttp.ClientSession() as session:
                tasks = []
                for i, u in enumerate(urls):
                    task = asyncio.create_task(download_one_image(session, u, i, path, successes, failures))
                    tasks.append(task)
                    counter_links += 1
                    print(f"Добавлено ссылок: {counter_links}")
            if tasks:
                await asyncio.gather(*tasks)
    return successes, failures

def main():
    # os.system('cls' if os.name == 'nt' else 'clear')
    successes = []
    failures = []
    path = create_folder()
    successes, failures = asyncio.run(collect_links(session, path, successes, failures))
    print("\nУспешные загрузки:")
    for url in successes:
        print (url)
    print("\nОшибки:")
    for url, err in failures:
        print(f"{url} - {err}")

if __name__=="__main__":
    main()