# Video Storage Application

This project serves as a learning exercise for building a video storage application using Flask and Deta Space. The application allows users to download videos from YouTube, upload them to a cloud storage service (Deta), and manage video metadata in a CSV file.

## Features

- **Download Videos**: Download videos from YouTube using `yt-dlp`.
- **Upload to Deta**: Upload videos to Deta Space for cloud storage.
- **Manage Metadata**: Store video metadata (video ID, date uploaded, original link, uploaded URL) in a CSV file.
- **Stream Videos**: Stream videos from Deta Space via a Flask web server.

## Usage

1. **Setup**:
   - Clone the repository: `git clone https://github.com/WhoIsJayD/Youtube-x-Deta-Learning-Project`
   - Install dependencies: `pip install -r requirements.txt`
   
2. **Configuration**:
   - Set up a Deta account and create a new project.
   - Replace `"Removed_Updating_Visibility_Of_Repo"` in `app.py` with your Deta project key.

3. **Run**:
   - Run the application: `python app.py`
   - Access the application at `http://localhost:5000`

## Contact

For any inquiries or permissions, please contact:

- **Name**: Jaydeep Solanki
- **Email**: jaydeep.solankee@yahoo.com
- **LinkedIn**: [Jaydeep Solanki LinkedIn](https://www.linkedin.com/in/jaydeep-solanki-79ab61253/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

