import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TTS import TTSGenerator

class RedditStoryScraper:
    def __init__(self, chromedriver_path, stories_dir):
        self.chromedriver_path = chromedriver_path
        self.stories_dir = stories_dir
        self.identifier=None
        if not os.path.exists(self.stories_dir):
            os.makedirs(self.stories_dir)
        self.driver = None

    def _setup_driver(self):
        service = Service(executable_path=self.chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)

    def scrape_story(self, url):
        full_text = ''
        try:
            self._setup_driver()
            self.driver.get(url)

            identifier = url.split('/comments/')[1].split('/')[0]
            self.identifier=identifier
            
            div_id = f"t3_{identifier}-post-rtjson-content"
            h1_id = f"post-title-t3_{identifier}"
            

            h1_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, h1_id)))
            title = h1_element.text
                # Construct the button id
            button_id = f"t3_{identifier}-read-more-button"

            try:
                # Wait for the "Read more" button to be clickable and click it
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, button_id))
                ).click()
            except:
                pass
            
            time.sleep(5)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, div_id))
            )

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, div_id)))
            div_element = self.driver.find_element(By.ID, div_id)
            paragraphs = div_element.find_elements(By.TAG_NAME, "p")

            with open(os.path.join(self.stories_dir, f"story_{identifier}.txt"), "w") as file:
                for paragraph in paragraphs:
                    text = paragraph.text + "\n"
                    file.write(text)
                    full_text += text
            self.close_driver()

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                # self.close_driver()

        return title, full_text

    def split_text_into_chunks(self, pathToStory, chunk_size=490):
        storyAudioFoldPath=f'C:\Projects\Reddit Bot\Audio Files\{self.identifier}'
        os.makedirs(storyAudioFoldPath, exist_ok=True)
        with open(pathToStory, 'r') as file:
            text = file.read()
        words = text.split()
        chunks = []
        current_chunk = ""
        chunkIndex=0
        

        for word in words:
            if len(current_chunk) + len(word) + 1 > chunk_size:
                chunks.append(current_chunk)
                current_chunk = word
            else:
                current_chunk += " " + word if current_chunk else word

        if current_chunk:
            chunks.append(current_chunk)

        TTSFile = TTSGenerator(chromedriver_path="C:\\Driver\\chromedriver.exe")
        for chunkIndex, chunk in enumerate(chunks):
            TTSFile.generate_audio(chunk, storyAudioFoldPath+f'\practice{chunkIndex}.mp3')
        TTSFile.close_driver()
        TTSFile.merge_audio_files(storyAudioFoldPath)
        return chunks

# Example usage
scraper = RedditStoryScraper("C:\\Driver\\chromedriver.exe", "C:\\Projects\\Reddit Bot\\Stories")
title, story = scraper.scrape_story("https://www.reddit.com/r/TrueOffMyChest/comments/16q658o/wife_told_me_last_night_i_have_a_small_penis/")
scraper.split_text_into_chunks(f'C:\Projects\Reddit Bot\Stories\story_{scraper.identifier}.txt')
