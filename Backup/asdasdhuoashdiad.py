import csv
import os
import subprocess
import time
import uuid
from datetime import datetime

from deta import Deta
from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

# Initialize Deta project
deta = Deta("d0AG6dLw5EAs_3KVUpWfLLNGrA73MRtPoZRAwPkvRxJH1")

# Set up Deta base
db = deta.Drive("video_storage")


def download_video(url):
    # Generate a unique ID for the video
    video_id = str(uuid.uuid4())

    # Download video using yt-dlp in the best quality with mp4 extension
    command = ["yt-dlp", url, "-o", f"{video_id}.%(ext)s", "-f",
               "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"]
    subprocess.call(command)

    return video_id


def upload_video(file_path, video_id):
    # Upload the video file to Deta Space
    response = db.put(video_id, open(file_path, "rb"))
    return response


def download_file(video_id):
    # Retrieve the video data from Deta Space
    video_data = db.get(video_id)

    # Write the video data to a local file
    file_path = f"{video_id}_downloaded.mp4"
    with open(file_path, "wb") as file:
        for chunk in video_data.iter_chunks():
            file.write(chunk)

    return file_path


def delete_file(file_path):
    # Delete the file from the local device
    os.remove(file_path)


def update_csv(video_id, url, original_link):
    # Get current date and time
    date_uploaded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the CSV file already exists
    csv_file_exists = os.path.isfile("videos.csv")

    # Write the video information to the CSV file
    with open("videos.csv", mode="a") as csv_file:
        fieldnames = ["Video ID", "Date Uploaded", "Original Link", "Uploaded URL"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header if the CSV file doesn't exist
        if not csv_file_exists:
            writer.writeheader()

        writer.writerow({
            "Video ID": video_id,
            "Date Uploaded": date_uploaded,
            "Original Link": original_link,
            "Uploaded URL": url
        })


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the video URL from the form
        video_url = request.form.get("video_url")
        print(video_url)


        # Download the video and get the video ID
        video_id = download_video(video_url)

        # Modify the file path to include the correct file extension
        file_path = f"{video_id}.mp4"

        # Upload the video to Deta Space
        response = upload_video(file_path, video_id)

        # Delete the local file
        delete_file(file_path)

        # Update the CSV file with video information
        update_csv(video_id, response, video_url)

        # Reload the page
        return redirect(url_for("index"))

    # Get a list of all items in the Deta drive
    items = db.list()

    return render_template("index.html", items=items["names"])


@app.route("/video/<video_id>")
def stream_video(video_id):
    time.sleep(0.2)
    video_data = db.get(video_id)

    # Set the appropriate headers for seeking support
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "video/mp4"
    }

    def generate(video_data):
        for chunk in video_data.iter_chunks():
            yield chunk

    # Stream the video data as a response
    return Response(generate(video_data), mimetype="video/mp4", headers=headers)


if __name__ == "__main__":
    app.run(debug=True)
