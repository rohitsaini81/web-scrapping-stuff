import time
from create import *
from download import *
import requests
# from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
url = 'https://hotxv.com'
# url2 = 'https://hotxv.com/video-7ekhw7kkn1v/she-fucked-her-bestie-s-boyfriend-after-party-and-don-t-regret-about-it.html'


def extract_video(vid_url):

    html_content = scrape(vid_url)
    soup = BeautifulSoup(html_content, "html.parser")
    for div in soup.find_all("video"):
        source_tag = div.find("source")
        if source_tag:
            return source_tag["src"]
        else:
            return "not found or error "


def extract_data():
    html_content = scrape()
    print("Extracting...")
    soup = BeautifulSoup(html_content, "html.parser")
    videos = []

    # Find all video containers
    for div in soup.find_all("div", class_="w3-third w3-container w3-margin-bottom"):
        title_tag = div.find("p")
        img_tag = div.find("img")
        span_tag = div.find("span")
        anchor_tag = div.find("a")

        if title_tag and img_tag and span_tag and anchor_tag:
            title = title_tag.text.strip()
            duration = span_tag.text.strip().split(":", 1)
            img_url = img_tag["src"]
            video_url = anchor_tag["href"]
            videos.append(
                {"title": title, "Duration": duration[1], "image": img_url, "video": video_url})

    # Print extracted data
    for video in videos:

        title = f"{video['title']}"
        image = f"https://www.hotxv.com{video['image']}"
        
        print("Extracting from Preview page...")
        video_url = f"https://www.hotxv.com{video['video']}"
        new_video_url = extract_video(video_url)
        
        final_img_url = downloads(image, True)
        image = final_img_url 

        final_video_url=  download_file(new_video_url, False)
        new_video_url = final_video_url
        print("-" * 40)
        
        tags = ["porn"]
        
        description = "test"
        
        category = ["porn"]
        
        duration = f"{video['Duration']}"

        

        if title is None or image is None or new_video_url is None or tags is None or description is None or category is None or duration is None:
            print("Error: Missing data")
            print("title", title)
            print("image", image)
            print("video", new_video_url)
            print("tags", tags)
            print("description", description)
            print("category", category)
            print("duration", duration)
            print("-" * 40)
            
        else:
            print("Creating data...")
            print("-" * 40)
            create_video(title, image, new_video_url, tags, description, category, duration)
            time.sleep(1)


def set_links(i):
    print("Reading Database...")
    maindata = read_videos()
    count = 0
    if maindata is None:
        print("Error: No data to process.")
    else:
        for row in maindata:
            try:
                isImage = True
                print(count)
                print(" -" * 40)
                time.sleep(1)
                count += 1
                link = row[i]
                print("link : "+link)
            
                if i == 7:
                    isImage = False
                download_file(link, isImage)
            except Exception as e:
                print(f"Error processing row: {row}, Error: {e}")
                continue


def scrape(url_to_scrape=url):
    response = requests.get(url_to_scrape)
    if response.status_code == 200:
        html_content = response.text
        return html_content
        # extractdata(html_content)
    else:
        print(
            f"Failed to retrieve the webpage. Status code: {response.status_code}")


def main():
    print("Starting...")
    extract_data()
    print("Setting Images")
    # set_links(6)
    # print("Setting Videos")
    # set_links(7)


if __name__ == "__main__":
    main()
