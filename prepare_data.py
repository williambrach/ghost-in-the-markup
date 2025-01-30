import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

SERVER_URL = "127.0.0.1:8000"
TRUE_PATH = "src\\data\\true"
GENERATED_PATH = "src\\data\\generated"
METHODS = ["prompt_injection", "iframe", "obfuscation", "true"]  # "random_elements"

folders = [
    f for f in os.listdir(TRUE_PATH) if os.path.isdir(os.path.join(TRUE_PATH, f))
]

# check if generated folder exists; if not, create folder
if not os.path.exists(GENERATED_PATH):
    os.makedirs(GENERATED_PATH)

async def save_content(content: str, save_folder_path: str) -> None:
    soup = BeautifulSoup(content, "html.parser")
    with open(save_folder_path, "w") as f:
        f.write(str(soup))

async def scrape_page(
    page: object, file_path: str, method: str, save_folder_path: str
) -> None:
    if method == "true":
        url = f"http://{SERVER_URL}?file_path={file_path}"
    else:
        url = f"http://{SERVER_URL}?file_path={file_path}&method={method}"

    try:
        await page.goto(url, timeout=60000, wait_until="networkidle")
        content = await page.content()
        await save_content(content, save_folder_path)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        for folder in folders:
            files = [
                f
                for f in os.listdir(os.path.join(TRUE_PATH, folder))
                if os.path.isfile(os.path.join(TRUE_PATH, folder, f))
            ]
            for file in files:
                if "json" in file:
                    continue
                file_path = os.path.join(folder, file)
                file_path = file_path.replace("\\", "/")
                print(file_path)
                for method in METHODS:
                    save_folder_path = os.path.join(GENERATED_PATH, folder, method)
                    if not os.path.exists(save_folder_path):
                        os.makedirs(save_folder_path)
                    save_folder_path = os.path.join(save_folder_path, file)
                    await scrape_page(page, file_path, method, save_folder_path)
        await browser.close()
    print("Scraping completed.")

# Execute the main function
  # noqa: PLE1142

import asyncio  
async def m():
    await main()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())