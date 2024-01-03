import requests
import time
import os

from pydub import AudioSegment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import quote

class TTSGenerator:
    def __init__(self, chromedriver_path="C:\\Driver\\chromedriver.exe"):
        self.chromedriver_path = chromedriver_path
        self.driver = None
    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    def generate_audio(self, text, output_file):
        driver = None
        try:
            encoded_text = quote(text)
            url = f"https://lazypy.ro/tts/?voice=Joanna&service=StreamElements&text={encoded_text}&lang=English&g=F"
            
            service = Service(executable_path=self.chromedriver_path)
            driver = webdriver.Chrome(service=service)
            driver.get(url)
            time.sleep(5)

            audio_element = driver.find_element(By.ID, "audioplayer")
            mp3_url = audio_element.get_attribute("src")

            response = requests.get(mp3_url)
            with open(output_file, "wb") as file:
                file.write(response.content)
            print(f"MP3 file downloaded: {output_file}")

        except Exception as e:
            print(f"Error occurred: {e}")

    def merge_audio_files(self,folder):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.mp3')]
        print(files)
        if not files:
            print("No MP3 files found in the folder.")
            return

        # Start with an empty audio segment
        combined = AudioSegment.empty()

        # Concatenate all files
        for file in files:
            next_audio = AudioSegment.from_file(file, format='mp3')
            combined += next_audio
            os.remove(file)

        # Export the combined audio file
        output_path = os.path.join(folder, f"{os.path.basename(folder)}.mp3")
        combined.export(output_path, format='mp3')
        print(f"Merged audio file created: {output_path}")

# # Example usage
# tts_generator = TTSGenerator("C:\\Driver\\chromedriver.exe")
# tts_generator.generate_audio("This is a test text", "downloaded_audio.mp3")
