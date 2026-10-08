import os
import subprocess
from pathlib import Path
import asyncio
import edge_tts

# 1. वीडियो डाउनलोड करने का फंक्शन (yt-dlp का उपयोग करके)
def download_video(url, output_filename="input_video.mp4"):
    print(f"Downloading video from {url}...")
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", output_filename,
        url
    ]
    subprocess.run(command, check=True)
    print("Video downloaded successfully!")
    return output_filename

# 2. वीडियो से ऑडियो अलग करने का फंक्शन
def extract_audio(video_path, audio_path="input_audio.wav"):
    print("Extracting audio from video...")
    command = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0",
        "-map", "a",
        audio_path,
        "-y"
    ]
    subprocess.run(command, check=True)
    print("Audio extracted successfully!")
    return audio_path

# 3. प्राकृतिक हिंदी आवाज़ (Human-like Voice) जनरेट करने का फंक्शन (Edge-TTS)
async def generate_hindi_voice(text, output_audio_path="dubbed_audio.mp3"):
    # 'hi-IN-SwaraNeural' माइक्रोसॉफ्ट की बहुत ही प्राकृतिक और मधुर हिंदी फीमेल आवाज़ है
    voice = "hi-IN-SwaraNeural"
    print(f"Generating natural human-like Hindi voice using {voice}...")
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)
    print("Dubbed audio generated successfully!")
    return output_audio_path

# 4. डब किए गए ऑडियो को वीडियो में जोड़ने का फंक्शन
def merge_audio_video(video_path, dubbed_audio_path, output_video_path="final_dubbed_video.mp4"):
    print("Merging dubbed audio with the video...")
    command = [
        "ffmpeg",
        "-i", video_path,
        "-i", dubbed_audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_video_path,
        "-y"
    ]
    subprocess.run(command, check=True)
    print(f"Final video created: {output_video_path}")
    return output_video_path

# मुख्य प्रक्रिया (Main Execution Pipeline)
async def main():
    # यहाँ अपना Dailymotion या किसी भी प्लेटफॉर्म का वीडियो लिंक डालें
    video_url = os.environ.get("VIDEO_URL", "YOUR_DAILYMOTION_VIDEO_URL_HERE")
    
    # स्टेप 1: वीडियो डाउनलोड करें
    video_file = download_video(video_url)
    
    # स्टेप 2: ऑडियो निकालें (यदि आपको ट्रांसक्रिप्शन या अनुवाद जोड़ना हो)
    audio_file = extract_audio(video_file)
    
    # स्टेप 3: हिंदी टेक्स्ट जिसे बुलवाना है (आप यहाँ अपना अनुवादित टेक्स्ट या स्क्रिप्ट दे सकती हैं)
    hindi_text = "नमस्ते! आपका इस वीडियो में स्वागत है। यह वीडियो अब पूरी तरह से प्राकृतिक हिंदी आवाज़ में डब किया जा चुका है।"
    
    # स्टेप 4: नेचुरल ह्यूमन जैसी हिंदी आवाज़ बनाएं
    dubbed_audio = await generate_hindi_voice(hindi_text)
    
    # स्टेप 5: नई आवाज़ को वीडियो के साथ मर्ज करें
    final_output = merge_audio_video(video_file, dubbed_audio)
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
