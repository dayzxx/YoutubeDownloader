\# YTube Downloader



A terminal-based YouTube downloader with a clean interface. Supports video in multiple qualities, audio-only downloads, playlist downloading, and manual format selection.



\---



\## Requirements



\- Python 3.8+

\- pip



> `yt-dlp` is installed automatically by `setup.py` — you don't need to install it manually.



\---



\## Installation



\*\*1. Clone the repository\*\*

```bash

git clone https://github.com/dayzxx/YoutubeDownloader.git

cd YoutubeDownloader

```



\*\*2. Run the setup script first\*\*

```bash

python setup.py

```



This installs `yt-dlp` and marks your environment as ready. You won't be able to run the downloader without doing this step first.



\---



\## Usage



```bash

python YoutubeDownloader.py

```



Then follow the prompts:



1\. Paste a YouTube URL (video or playlist)

2\. Choose a quality preset:

&#x20;  - Best quality (recommended)

&#x20;  - 1080p

&#x20;  - 720p

&#x20;  - 480p

&#x20;  - Audio only (mp3, 320kbps)

&#x20;  - Manual format selection

3\. Choose an output folder (defaults to `\~/Downloads`)

4\. Confirm and download



\---



\## File Structure



```

ytube-downloader/

├── YoutubeDownloader.py   # Main downloader script

├── setup.py               # Installs dependencies

├── .gitignore

└── README.md

```



\---



\## Notes



\- Playlists are supported — just paste the playlist URL

\- Audio-only downloads are saved as `.mp3` at 320kbps

\- Video downloads are merged and saved as `.mp4`

\- Re-run `setup.py` if yt-dlp ever stops working



\---



\*Made by dayzx\*

