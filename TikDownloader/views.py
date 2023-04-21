from django.views import View
from django.shortcuts import render
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen


def get_download_video(link, index):
    print(f"Загружаем видео {index} : {link}")
    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-US;q=0.8,tg;q=0.7,sv;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/de',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/de',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'de',
        'tt': 'Wk5Kbms1',
    }

    response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    mp4File = urlopen(downloadLink)

    with open(f"uploads/{ index if videoTitle =='' else videoTitle}.mp4", "wb") as file:
        while True:
            data = mp4File.read(4096)
            if data:
                file.write(data)
            else:
                break


class TikTokDownloadView(View):
    template_name = "TikDownloader/tiktok_download.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        nickname = request.POST["nickname"]

        driver = webdriver.Chrome()
        driver.get(f"https://www.tiktok.com/@{nickname}")

        time.sleep(10)

        scroll_pause_time = 1
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1

        print("Шаг 2: Scrolling page")
        while True:
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if screen_height * i > scroll_height:
                break

        soup = BeautifulSoup(driver.page_source, "html.parser")
        videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

        num_videos = len(videos)  # добавляем это
        context = {"num_videos": num_videos}  # добавляем это

        for index, video in enumerate(videos, start=1):
            print(f"Скачивается видео: {index}")
            url = video.a["href"]

            get_download_video(url, index)
            time.sleep(10)

        return render(request, self.template_name, context=context)