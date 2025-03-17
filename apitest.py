import time
from create import *
from download import *
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
# url = "http://127.0.0.1:5000/search"
url = 'https://hotxv.com'
url2 = 'https://hotxv.com/video-7ekhw7kkn1v/she-fucked-her-bestie-s-boyfriend-after-party-and-don-t-regret-about-it.html'

# data = {
#     "title": "Python",
#     "tags": "programming",
#     "keywords": "tutorial"
# }

# response = requests.post(url, json=data)
# print(response.json())


def extractvideo(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    for div in soup.find_all("video"):
        source_tag = div.find("source")
        if source_tag:
            return source_tag["src"]
        else:
            return "not found or error "


def extractdata(html_content):

    soup = BeautifulSoup(html_content, "html.parser")
    videos = []

    # Find all video containers
    for div in soup.find_all("div", class_="w3-third w3-container w3-margin-bottom"):
        title_tag = div.find("p")
        img_tag = div.find("img")
        span_tag = div.find("span")
        anchor_tag = div.find("a")

        if title_tag and img_tag or span_tag and anchor_tag:
            title = title_tag.text.strip()
            duration = span_tag.text.strip().split(":", 1)

            img_url = img_tag["src"]
            video_url = anchor_tag["href"]
            videos.append(
                {"title": title, "Duration": duration[1], "image": img_url, "video": video_url})

    # Print extracted data
    for video in videos:
        # print(f"Title: {video['title']}")
        # print(f"Duration: {video['Duration']}")
        title = f"{video['title']}"
        image = f"https://www.hotxv.com{video['image']}"
        video = f"https://www.hotxv.com{video['video']}"
        tags = ["porn"]
        description = "test"
        keywords = ["porn"]
        print(image)

        create_video(title, image, video, tags, description, keywords)
        time.sleep(1)
        print("-" * 40)


#response = requests.get(url)
#if response.status_code == 200:
    #html_content = response.text
    #print(extractdata(html_content))
    #extractdata(html_content)
#else:
#    print( f"Failed to retrieve the webpage. Status code: {response.status_code}")




maindata = read_videos()
count = 0

if maindata is None:
    print("Error: No data to process.")
else:
    for row in maindata:
        try:
            link = row[3]
            print(count)
            response = requests.get(link)
            if response.status_code == 200:
                html_content = response.text
                uri = extractvideo(html_content)
                #download_file(uri)
                print(uri)
                print("-" * 40)
                time.sleep(1)
                count += 1
            #download_file(row[2])
        except Exception as e:
            print(f"Error processing row: {row}, Error: {e}")
            continue



