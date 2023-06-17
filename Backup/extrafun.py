import yt_dlp
import csv
import os
from flask import Flask, render_template, Response

app = Flask(__name__)

def download_video(url):
    ydl_opts = {'format': 'mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_filename = ydl.prepare_filename(info_dict)
        ydl.download([url])
        return video_title, video_filename


def save_to_csv(video_title, video_filename):
    csv_filename = 'video_metadata.csv'

    # Retrieve file metadata
    file_size = os.path.getsize(video_filename)
    file_date = os.path.getctime(video_filename)

    # Write metadata and video bytes to CSV file
    with open(video_filename, 'rb') as file:
        video_bytes = file.read()

    with open(csv_filename, 'w', newline='', encoding='utf-8', errors='ignore') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'File Size', 'File Date'])
        writer.writerow([video_filename, file_size, file_date])
        writer.writerow([])  # Empty row
        writer.writerow(['Video Bytes'])
        writer.writerow([video_bytes])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    video_url = 'https://www.youtube.com/watch?v=29vYgKKtLjA'
    title, filename = download_video(video_url)
    save_to_csv(title, filename)

    # Retrieve video bytes from CSV file
    csv_filename = 'video_metadata.csv'
    with open(csv_filename, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    video_bytes_row_index = rows.index(['Video Bytes']) + 1
    video_bytes = rows[video_bytes_row_index][0]

    def generate():
        yield video_bytes

    headers = {
        'Accept-Ranges': 'bytes',
        'Content-Type': 'video/mp4'
    }

    return Response(generate(), mimetype='video/mp4', headers=headers)


if __name__ == '__main__':
    app.run()
