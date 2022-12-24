import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json


class TiktokScraper(webdriver.Chrome):
    def __init__(self, options=webdriver.ChromeOptions(), executable_path=r"C:/SeleniumDrivers/chromedriver.exe", teardown=False):
        self.teardown = teardown
        options.add_experimental_option("detach", True)
        service = Service(executable_path=executable_path)
        super().__init__(options=options, service=service)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()
            return super().__exit__(exc_type, exc, traceback)

    def land_page(self):
        self.get(
            "https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en")

    def filter_ads(self, filters):
        time.sleep(3)
        # find region list
        region_list = self.find_element(By.ID, "topadsRegion")
        # clear region list
        clear = self.find_element(
            By.XPATH, '//*[@id="topadsRegion"]/span/div/span')
        clear.click()

        region_list.click()
        self.click_from_list(filters["Region"])

        # find industry list
        industry_list = self.find_element(
            By.XPATH, '//*[@id="ccContentContainer"]/div[2]/div/div[1]/div/div[1]/div/div')
        industry_list.click()
        time.sleep(4)

        # find industry input
        industry_input = self.find_element(
            By.CSS_SELECTOR, "body > div:nth-child(45) > div > div > div > div > div.byted-cascader-popover-search-input > span > label > input")
        # search for industry
        industry_input.send_keys(filters["Industry"])

        # select first match
        industry = self.find_element(
            By.CSS_SELECTOR, 'div[role="rowgroup"] > div  span').click()

        # industry.find_element(By.CSS_SELECTOR, "span").click()

        # select remaining filters
        for key in filters.keys():
            if key not in ["Region", "Industry"]:
                self.find_element(By.ID, "topads"+key).click()
                self.click_from_list(filters[key])

    def click_from_list(self, filter):
        values = self.find_elements(
            By.CSS_SELECTOR, "div[data-type='select-option']")

        for value in values:
            if value.text == filter:
                value.click()

    def get_ad_info(self, filters):
        try:
            # try clicking on the "view more" button
            time.sleep(2)
            self.find_element(By.CLASS_NAME, "button--Zmt5a").click()
        except:
            pass

        # get all ads
        time.sleep(2)
        ads = self.find_elements(By.CLASS_NAME, "card-wrapper--7EOxZ")

        with open("ads.json", "w") as file:
            adds_dict = {}
            adds_dict["filters"] = filters
            adds_dict["links"] = []
            for i, ad in enumerate(ads, start=1):
                print("collecting ad", i)
                ad.click()
                self.switch_to.window(self.window_handles[1])
                time.sleep(3)
                adds_dict["ad"+str(i)] = {}
                info = self.find_elements(
                    By.CLASS_NAME, "info-content--kqx-4")[3:]
                adds_dict["ad"+str(i)]["Source"] = info[0].text
                adds_dict["ad"+str(i)]["Likes"] = info[1].text
                adds_dict["ad"+str(i)]["Comments"] = info[2].text
                adds_dict["ad"+str(i)]["Shares"] = info[3].text

                for idx, key in enumerate(["CVR", "CTR", "Clicks", "Conversions", "Remains"]):
                    button = self.find_element(
                        By.CSS_SELECTOR,
                        f'span[data-testid="cc_topads_detail_keyframe-{idx}"]'
                    )
                    button.click()
                    time.sleep(2)

                    adds_dict["ad"+str(i)][key] = \
                        self.find_element(
                        By.CSS_SELECTOR,
                        "span[class='labelBlackKey']").text + " of the industry average"

                # get video link
                video = self.find_element(By.CSS_SELECTOR, 'video')
                adds_dict["links"].append(video.get_attribute("src"))

                # close tab
                self.close()
                self.switch_to.window(self.window_handles[0])
                time.sleep(3)
            file.write(json.dumps(adds_dict))
        return adds_dict["links"]
