from flask import Flask, request, Response
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def get_random_problem_by_level(level):
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://school.programmers.co.kr/learn/challenges?order=recent&levels={level}"
    driver.get(url)
    time.sleep(2)

    problems = driver.find_elements(By.CSS_SELECTOR, '.bookmark a')

    if not problems:
        driver.quit()
        return None, None

    selected = random.choice(problems)
    title = selected.text.strip()
    link = selected.get_attribute('href')

    driver.quit()
    return title, link

@app.route('/coding_test', methods=['GET'])
def coding_test():
    level = request.args.get('level', default='2')
    title, link = get_random_problem_by_level(level)

    if not title or not link:
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "❌ 해당 난이도의 문제를 찾을 수 없습니다."
                        }
                    }
                ]
            }
        }
    else:
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"📌 {title}\n🔗 {link}"
                        }
                    }
                ]
            }
        }

    return Response(
        json.dumps(response, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
