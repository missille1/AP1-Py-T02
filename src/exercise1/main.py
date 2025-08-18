import os
import aiohttp
import asyncio
from prettytable import PrettyTable

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

async def download_one_image(session, u, i, path, result):
    done = True
    content = None
    resp = None
    file_path = os.path.join(path, f"img_{i+1}.jpg") 
    
    try:
        resp =  await session.get(u) #  асинхронный HTTP‑запрос к адресу файл + статус ответа
    except aiohttp.ClientError:
        result.append((i, u, "Ошибка"))
        done = False
        resp = None

    if done and resp is not None and resp.status != 200 :
        result.append((i, u, "Ошибка"))
        done = False

    if done and resp is not None:
        content = await resp.read()
        content_type = resp.headers.get("Content-Type", "")
        if not content or not content_type.startswith("image/"): 
            result.append((i, u, "Ошибка"))
            done = False

    if done and content is not None:
        f = open(file_path, 'wb')
        written = f.write(content)
        f.close()
        if written == 0:
            result.append((i, u, "Ошибка"))
            done = False

    if done:
        result.append((i, u, "Успех"))

async def collect_links(path, result):
    link = None
    tasks = []
    done = True
    i = 0
    
    async with aiohttp.ClientSession() as session:
        while done:
            link = (await asyncio.to_thread(input)).strip()
            if link == '':
                done = False
            else:
                tasks.append(asyncio.create_task(
                    download_one_image(session, link, i, path, result)))
                i += 1   
        if tasks:
            await asyncio.gather(*tasks)
    return result

def print_results(results):
    # вернуть исходный порядок ввода
    results.sort(key=lambda x: x[0]) # сортировка по первому элементу
    table = PrettyTable()
    table.field_names = ["Ссылка", "Статус"]
    # выравнивание по левому краю
    table.align["Ссылка"] = "l"
    for _, url, status in results:
        table.add_row([url, status])
    print(table)

def main():
    result = []
    path = create_folder()
    result = asyncio.run(collect_links(path, result))
    
    print_results(result)

if __name__=="__main__":
    main()