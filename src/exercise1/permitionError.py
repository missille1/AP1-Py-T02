import os
import asyncio
import aiohttp

def create_folder():
    done = True
    path = None
    while done:
        path = input()
        if '..' in path:
            print("Вы можете создать папку только в папке src/")
        elif not os.path.exists(path):
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
        timeout = aiohttp.ClientTimeout(total=20)
        resp = await session.get(u, timeout=timeout)
    except (aiohttp.ClientError, asyncio.TimeoutError):
        failures.append((u, "Ошибка сети/таймаут"))
        done = False
        resp = None

    if done and (resp is None or resp.status != 200):
        code = None if resp is None else resp.status
        failures.append((u, f"HTTP {code}"))
        done = False

    if done:
        try:
            content = await resp.read()
        finally:
            if resp is not None:
                await resp.release()
        ctype = resp.headers.get("Content-Type", "")
        if not content or not ctype.startswith("image/"):
            failures.append((u, "Не изображение или пустой ответ"))
            done = False

    if done:
        try:
            with open(file_path, 'wb') as f:
                written = f.write(content)
            if written == 0:
                failures.append((u, "Не удалось записать файл"))
                done = False
        except PermissionError:
            failures.append((u, "Недостаточно прав на запись"))
            done = False
        except OSError as e:
            failures.append((u, f"Ошибка записи: {e}"))
            done = False

    if done:
        successes.append(u)
    return None

async def _async_input(prompt: str = "") -> str:
    # неблокирующее чтение: input() в отдельном потоке
    return await asyncio.to_thread(input, prompt)

# ---- единственная async-функция верхнего уровня ----
async def collect_links(path, successes, failures):
    headers = {"User-Agent": "img-loader/1.0"}
    tasks = []
    collecting = True
    i = 0
    counter_links = 0

    # создаём session здесь, внутри async‑функции
    async with aiohttp.ClientSession(headers=headers) as session:
        while collecting:
            link = (await _async_input()).strip()
            if link == '':
                collecting = False
            else:
                tasks.append(asyncio.create_task(
                    download_one_image(session, link, i, path, successes, failures)
                ))
                i += 1
                counter_links += 1
                print(f"Добавлено ссылок: {counter_links}")

        if tasks:
            await asyncio.gather(*tasks)

    return successes, failures  # один выход

# ---- синхронный main ----
def main():
    successes, failures = [], []
    path = create_folder()
    # запускаем ТОЛЬКО collect_links в event loop
    successes, failures = asyncio.run(collect_links(path, successes, failures))

    print("\nУспешные загрузки:")
    for url in successes:
        print(url)
    print("\nОшибки:")
    for url, err in failures:
        print(f"{url} - {err}")
    return 0

if __name__ == "__main__":
    main()
