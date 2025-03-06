from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.devtools.v85.dom import highlight_rect

from inputs import input_str, input_choice

def get_paragraphs(browser):
    paragraphs = [p.text.strip() for p in browser.find_elements(By.TAG_NAME, "p") if p.text.strip() !=""]
    # for i,p in enumerate(paragraphs):
    #     if p.text=="": paragraphs[i].pop()

    p_quantity = len(paragraphs)
    return paragraphs, p_quantity

def get_links(browser):
    body_content = browser.find_elements(By.ID, "bodyContent")
    if body_content:
        body_content=body_content[0]
        toc_content = body_content.find_elements(By.ID, "toc")
    else:
        return [],[]
    if toc_content:
        toc_content = toc_content[0]
        toc_links = []
        for element in toc_content.find_elements(By.TAG_NAME, "a"):
            href = element.get_attribute("href")
            if href:
                toc_links.append((element.text.strip(), href))
                number = element.find_element(By.CLASS_NAME, "tocnumber").text
                if not number: number = ""
                text = element.find_element(By.CLASS_NAME, "toctext").text
                if not text: text = ""
                toc_links.append([f"{number} {text}".strip() if number or text else link.text.strip(), href])
    else:
        toc_links = None

    raw_links = body_content.find_elements(By.XPATH, './/a[not(ancestor::div[contains(@class, "reflist")]) and not(ancestor::div[@id="toc"]) and not(starts-with(@href, "#cite"))]')

    links = []

    for element in raw_links:
        href = element.get_attribute("href")
        if href and "/w/index.php" not in href and "#" not in href:
            text = element.text.strip()
            if text:
                links.append((text, href))

    return links,toc_links



users_search = input_str("Введите поисковую фразу: ")
num = 0
choice = None
browser = webdriver.Chrome()
browser.get(
    "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
search_input = browser.find_element(By.ID, "searchInput")
search_input.send_keys(users_search)
search_input.send_keys(Keys.ENTER)

while choice != "4":
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "bodyContent")))
    prompt = ("Выберите вариант:\n"
              "1. Листать параграфы\n"
              "2. Перейти к связанной статье\n"
              "3. Перейти  по содержанию\n"
              "4. Выход\n")
    paragraphs, p_quantity = get_paragraphs(browser)
    links,toc = get_links(browser)



    while True:
        choice = input_choice(["1", "2", "3", "4", ], prompt)
        if choice == "4":
            break
        elif choice == "1":
            if not paragraphs:
                print("Параграфы отсутствуют")
                continue
            print(paragraphs[num])
            num += 1
            if num == p_quantity:
                num = 0
                print("Параграфы закончились, перехожу на начало")
        elif choice == "2":
            if links:
                choice_link = input_choice([str(i) for i in range(1, len(links)+1)], "Выберите ссылку:\n"+"\n".join([f"{i+1}. {links[i][0]}" for i in range(len(links))])+"\n")
                browser.get(links[int(choice_link) - 1][1])
                break
            pass
        elif choice == "3":
            if toc:
                choice_toc = input_choice([str(i) for i in range(1, len(toc)+1)], "Выберите раздел:"+"\n".join([f"{i+1}. {toc[i][0]}" for i in range(len(toc))])+"\n")
                browser.get(toc[int(choice_toc)-1][1])
                continue
            else:
                print("Содержание отсутствует")
            pass
    if choice == 4:
        break

#browser.quit()
