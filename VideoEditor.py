import subprocess
import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip

class VideoEditor:
    def __init__(self, video_folder):
        self.video_folder = video_folder

    def get_random_video_file(self):
        video_files = [file for file in os.listdir(self.video_folder) if file.endswith('.mp4')]
        if not video_files:
            raise FileNotFoundError("No video files found in the folder.")
        return os.path.join(self.video_folder, random.choice(video_files))

    def overlay_audio(self, audio_file_path, output_video_path, speed_up_factor=1.08):
        try:
            video_file_path = self.get_random_video_file()
            video_clip = VideoFileClip(video_file_path)

            # Prepare the sped-up audio file path
            sped_up_audio_path = "sped_up_audio.mp3"

            # Use ffmpeg to speed up audio without changing pitch
            cmd = [
                'ffmpeg', '-i', audio_file_path,
                '-filter:a', f'atempo={speed_up_factor}',
                '-vn', sped_up_audio_path
            ]
            subprocess.run(cmd, check=True)

            # Load the sped-up audio into moviepy
            processed_audio_clip = AudioFileClip(sped_up_audio_path)

            # Trim video to match audio duration
            video_clip = video_clip.set_duration(processed_audio_clip.duration)

            # Set processed audio to video
            final_clip = video_clip.set_audio(processed_audio_clip)

            # Export the final video
            final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

            print(f"Video with processed audio overlay created: {output_video_path}")

            # Cleanup temporary audio file
            os.remove(sped_up_audio_path)

        except Exception as e:
            print(f"Error: {e}")

# Example usage
# Example usage
video_editor = VideoEditor("C:\Projects\Reddit Bot\Tetris Clips")
video_editor.overlay_audio("C:\\Projects\\Reddit Bot\\Audio Files\\z2ep2g\\z2ep2g.mp3", r"C:\Projects\Reddit Bot\Audio Files\z2ep2g\z2ep2g.mp4")
