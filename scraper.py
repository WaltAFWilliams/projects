from typing import List, Any

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import html5lib
import numpy as np, pandas as pd

class Scraper():
    def __init__(self):
        self.d = webdriver.Chrome()
        self.d.get("http://www.yelp.com/")

    def search_for_links(self, search_term):
        elem = self.d.find_element_by_id("find_desc")
        elem.clear()
        elem.send_keys(search_term)
        elem.send_keys(Keys.ENTER)
        review_pages = self.get_review_pages()
        homepages = self.get_homepage_links(review_pages)
        print(homepages, len(homepages), sep="\n\n")

    def get_review_pages(self):
        review_pages = []
        # Parsing first page
        source = self.d.page_source
        soup = BeautifulSoup(source, "html5lib")
        page_links = soup.findAll("a", attrs={"class": "lemon--a__373c0__IEZFH link__373c0__1G70M pagination-link-component__373c0__9aHoC link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"})
        all_review_links = soup.findAll("a", attrs={
            "class": "lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"})
        assert len(all_review_links) > 0 and len(page_links) > 0, "Found no review links to record"
        for page in all_review_links:
            hlink = page.attrs["href"]
            if hlink.startswith("/biz"):
                review_pages.append(hlink)

        # Parsing subsequent pages
        for num in page_links:
            print("STARTING NEW PAGE...\n\n")
            link = "https://www.yelp.com/" + num.attrs["href"]
            self.d.get(link)
            source = self.d.page_source
            soup = BeautifulSoup(source, "html5lib")
            all_review_links = soup.findAll("a", attrs={"class":"lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"})
            assert len(all_review_links)>0 and len(page_links)>0, "Found no review links to record"
            for page in all_review_links:
                hlink = page.attrs["href"]
                if hlink.startswith("/biz"):
                    review_pages.append(hlink)

        return review_pages

    def get_homepage_links(self, review_pages):
        homepages = []
        # Open links to the review pages then extract homepage link
        for page in review_pages:
            try: self.d.get("https://www.yelp.com/" + page)
            except Exception as e:
                print("Error " + page)
                homepages.append("Error: " + page)
                continue

            source = self.d.page_source
            soup = BeautifulSoup(source, "html5lib")
            all_links = soup.findAll("a", attrs={"class": "lemon--a__373c0__IEZFH link__373c0__1G70M link-color--blue-dark__373c0__85-Nu link-size--inherit__373c0__1VFlE"})       
            for l in all_links:
                if l.attrs["href"].startswith("/biz_redir"):
                    print(l.text)
                    homepages.append(l.text)
            
        return homepages

s = Scraper()
s.search_for_links("wine")
