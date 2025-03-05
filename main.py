from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from inputs import input_str, input_choice

def get_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    p_quantity = len(paragraphs)
    return paragraphs, p_quantity

def get_links(browser):
    links = browser.find_elements(By.TAG_NAME, "a")
    for i,link in enumerate(links):
        if link.get_attribute("href")[0] =="#":
            links.pop(i)
    prompt = "Ссылки:\n"
    choices = [str(i+1) for i in range(len(links))]
    for i,link in enumerate(links):
        prompt += f"{i+1}. {link.text}\n"

    return links, prompt, choices


users_search = input_str("Введите поисковую фразу: ")
browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
search_input = browser.find_element(By.ID, "searchInput")
search_input.send_keys(users_search)
search_input.send_keys(Keys.ENTER)
prompt = ("Выберите вариант:"
          "1. Листать параграфы" 
          "2. Перейти  по содержанию"
          "3. Перейти к связанной статье"
          "4. Выход")
paragraphs, p_quantity = get_paragraphs(browser)
links = get_links(browser)
num=0

while True:
    choice = input_choice(["1","2","3","4",], prompt)
    if choice == "4":
        break
    elif choice == "1":
        print(paragraphs[num].text)
        num += 1
        if num == p_quantity:
            num = 0
            print("Параграфы закончились, перехожу на начало")
    elif choice == "2":
        pass
    elif choice == "3":
        link = input_choice(links[2], links[1])
        browser.get(links[0][int(link)-1].get_attribute("href"))
        pass


#browser.quit()
