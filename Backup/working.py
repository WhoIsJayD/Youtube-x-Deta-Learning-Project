from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    with open(r"G:\Projects\Extraordinary\bcdd68c6-7b50-47a0-a378-47565f8d9fd7_downloaded.mp4", "rb+") as file:
        video_bytes = file.read() 

    def generate():
        yield video_bytes

    headers = {
        'Accept-Ranges': 'bytes',
        'Content-Type': 'video/mp4'
    }
    return Response(generate(), mimetype='video/mp4', headers=headers)

if __name__ == '__main__':
    app.run()
