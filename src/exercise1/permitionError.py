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

async def download_one_image(session, u, i, path, successes, failures):
    done = True
    content = None
    file_path = os.path.join(path, f"img_{i+1}.jpg") 
    
    try:
        resp = await session.get(u)  # асинхронный HTTP‑запрос
    except aiohttp.ClientError:
        failures.append((u, "Ошибка скачивания"))
        done = False
        resp = None

    if done and resp is not None and resp.status != 200:
        failures.append((u, f"HTTP {resp.status}"))
        done = False

    if done and resp is not None:
        content = await resp.read()
        content_type = resp.headers.get("Content-Type", "")
        if not content or not content_type.startswith("image/"): 
            failures.append((u, "Нет данных для записи"))
            done = False

    # Блок записи с обработкой PermissionError
    if done and content is not None:
        try:
            f = open(file_path, 'wb')
            written = f.write(content)
            f.close()
            if written == 0:
                failures.append((u, "Не удалось записать файл"))
                done = False
        except PermissionError:
            failures.append((u, "Нет прав на запись в каталог"))
            done = False

    if done:
        successes.append(u)

async def download_all_images(path, urls):
    successes = []
    failures = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, u in enumerate(urls):
            task = asyncio.create_task(download_one_image(session, u, i, path, successes, failures))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return successes, failures

def main():
    path = create_folder()
    urls = collect_links()
    successes, failures = asyncio.run(download_all_images(path, urls))
    print("\nУспешные загрузки:")
    for url in successes:
        print(url)
    print("\nОшибки:")
    for url, err in failures:
        print(f"{url} - {err}")

if __name__ == "__main__":
    main()
