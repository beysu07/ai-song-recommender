# Project Song

A simple Flask web application that suggests songs from Spotify based on the user's mood or intent. Users can input a description of their current state, and the application will return a relevant song.

## Features

- **Spotify Integration**: Connects to the Spotify API to search for playlists and songs.
- **Mood-Based Suggestions**: Analyzes user input to determine a mood and suggests songs accordingly.
- **Dynamic Playlist Selection**: Selects playlists based on the detected mood and desired time period (e.g., 2000s Turkish pop, 2010s global hits).

## Setup

Follow these steps to set up and run the application locally:

### Prerequisites

- Python 3.x
- pip (Python package installer)
- A Spotify Developer Account: You will need to create an application on the Spotify Developer Dashboard to obtain a `Client ID` and `Client Secret`.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd project-song
    ```
    (Note: Replace `<repository_url>` with the actual URL when you upload to GitHub)

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

The application requires Spotify API credentials. Create a `.env` file in the root directory of the project with the following content:

```
SPOTIFY_CLIENT_ID="your_spotify_client_id"
SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
```

Replace `"your_spotify_client_id"` and `"your_spotify_client_secret"` with the credentials from your Spotify Developer application.

## Usage

1.  **Run the Flask application**:
    ```bash
    python app.py
    ```

2.  **Access the application**:
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

3.  **Get song suggestions**:
    Enter your mood or intent in the provided text box and click "Get Song". The application will display a song suggestion.
