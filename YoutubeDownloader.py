import subprocess
import sys
import os
import re
import pathlib

SENTINEL = pathlib.Path(__file__).parent / ".setup_done"

RED     = "\033[91m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
 
LOGO = f"""
{RED}██╗   ██╗{WHITE}████████╗{RED}██╗   ██╗██████╗ ███████╗
{RED}╚██╗ ██╔╝{WHITE}╚══██╔══╝{RED}██║   ██║██╔══██╗██╔════╝
{RED} ╚████╔╝ {WHITE}   ██║   {RED}██║   ██║██████╔╝█████╗
{RED}  ╚██╔╝  {WHITE}   ██║   {RED}██║   ██║██╔══██╗██╔══╝
{RED}   ██║   {WHITE}   ██║   {RED}╚██████╔╝██████╔╝███████╗
{RED}   ╚═╝   {WHITE}   ╚═╝   {RED} ╚═════╝ ╚═════╝ ╚══════╝
{GRAY}         Downloader v1.0  —  by dayzx{RESET}
"""
 
SEPARATOR = f"{GRAY}{'─' * 58}{RESET}"
 
 
def clear():
    os.system("cls" if os.name == "nt" else "clear")
 
 
def print_header():
    clear()
    print(LOGO)
    print(SEPARATOR)
 
 
def check_ytdlp():
    if not SENTINEL.exists():
        print(f"\n{RED}Setup has not been run yet.{RESET}")
        print(f"{YELLOW}Please run setup.py first:{RESET}")
        print(f"  {CYAN}python setup.py{RESET}\n")
        sys.exit(1)

    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print(f"\n{YELLOW}  yt-dlp is missing despite setup being run.{RESET}")
        print(f"{RED}  Please re-run setup.py.{RESET}")
        SENTINEL.unlink(missing_ok=True)
        sys.exit(1)
 
 
def get_formats(url: str) -> list[dict]:
    print(f"\n{CYAN}Fetching available formats…{RESET}")
    result = subprocess.run(
        ["yt-dlp", "-F", url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"{RED}  Error: {result.stderr.strip()}{RESET}")
        return []
 
    lines = result.stdout.splitlines()
    formats = []
    for line in lines:
        m = re.match(r"^(\d+)\s+(\S+)\s+(\S+)\s+(.*)", line)
        if m:
            fmt_id, ext, resolution, note = m.groups()
            formats.append({
                "id": fmt_id,
                "ext": ext,
                "resolution": resolution,
                "note": note.strip(),
                "raw": line.strip(),
            })
    return formats
 
 
def display_formats(formats: list[dict]):
    print(f"\n{BOLD}{WHITE}  Available formats:{RESET}\n")
    for i, f in enumerate(formats, 1):
        res_col = f"{YELLOW}{f['resolution']:>10}{RESET}"
        ext_col = f"{CYAN}{f['ext']:<5}{RESET}"
        id_col  = f"{GRAY}[{f['id']:>4}]{RESET}"
        note    = f"{GRAY}{f['note'][:40]}{RESET}"
        print(f"  {i:>3}. {id_col}  {ext_col}  {res_col}  {note}")
 
 
def preset_menu() -> str:
    print(f"\n{BOLD}{WHITE}  Quick quality:{RESET}\n")
    presets = [
        ("1", "Best quality video + audio  (recommended)   ", "bestvideo+bestaudio/best"),
        ("2", "1080p  (mp4)                                 ", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
        ("3", "720p   (mp4)                                 ", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
        ("4", "480p                                         ", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
        ("5", "Audio only  (mp3, 320kbps)                   ", "bestaudio"),
        ("6", "Choose manually from all formats             ", "__manual__"),
    ]
    for key, label, _ in presets:
        print(f"  {YELLOW}{key}{RESET}. {WHITE}{label}{RESET}")
 
    choice = input(f"\n{WHITE}Your choice: {RESET}").strip()
    for key, _, fmt in presets:
        if choice == key:
            return fmt
    print(f"{RED}Invalid choice, falling back to best quality.{RESET}")
    return "bestvideo+bestaudio/best"
 
 
def manual_format_selection(url: str) -> str:
    formats = get_formats(url)
    if not formats:
        return "bestvideo+bestaudio/best"
    display_formats(formats)
    fmt_id = input(f"\n{WHITE}Enter the format ID (e.g. 137): {RESET}").strip()
    valid_ids = {f["id"] for f in formats}
    if fmt_id in valid_ids:
        return fmt_id
    print(f"{RED}Invalid ID, using best quality.{RESET}")
    return "bestvideo+bestaudio/best"
 
 
def get_output_dir() -> str:
    default = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"\n{WHITE}Output folder {GRAY}[Enter = {default}]{WHITE}: {RESET}", end="")
    path = input().strip()
    if not path:
        path = default
    os.makedirs(path, exist_ok=True)
    return path
 
 
def download(url: str, fmt: str, output_dir: str, audio_only: bool = False, playlist: bool = False):
    print(f"\n{CYAN}Downloading…{RESET}\n")
    print(SEPARATOR)

    if playlist:
        output_template = f"{output_dir}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"
        cmd = ["yt-dlp", "-f", fmt, "--progress", "--yes-playlist", "-o", output_template]
    else:
        cmd = ["yt-dlp", "-f", fmt, "--progress", "--no-playlist", "-o", f"{output_dir}/%(title)s.%(ext)s"]

    if audio_only:
        cmd += ["--extract-audio", "--audio-format", "mp3", "--audio-quality", "0"]
    else:
        cmd += ["--merge-output-format", "mp4"]

    cmd.append(url)

    try:
        process = subprocess.run(cmd)
        print(SEPARATOR)
        if process.returncode == 0:
            print(f"\n{GREEN}{BOLD}Download complete!{RESET}")
            print(f"{GRAY}File saved to: {output_dir}{RESET}")
        else:
            print(f"\n{RED}An error occurred.{RESET}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Download cancelled.{RESET}")


def main():
    print_header()
    check_ytdlp()
    print_header()

    print(f"\n{WHITE}Paste the YouTube URL (or playlist):{RESET}")
    url = input(f"{CYAN}{RESET}").strip()
    if not url:
        print(f"{RED}Empty URL, aborting.{RESET}")
        sys.exit(0)

    print_header()
    print(f"\n{GRAY}URL: {url}{RESET}")
    fmt = preset_menu()

    audio_only = False
    if fmt == "__manual__":
        fmt = manual_format_selection(url)
    elif fmt == "bestaudio":
        audio_only = True

    print(f"\n{BOLD}{WHITE}  Playlist or single video?{RESET}\n")
    print(f"  {YELLOW}1{RESET}. {WHITE}Single video only{RESET}")
    print(f"  {YELLOW}2{RESET}. {WHITE}Full playlist{RESET}")
    playlist_choice = input(f"\n{WHITE}Your choice: {RESET}").strip()
    playlist_mode = playlist_choice == "2"

    output_dir = get_output_dir()

    print_header()
    print(f"\n  {BOLD}{WHITE}Summary:{RESET}")
    print(f"  {GRAY}URL   :{RESET} {url}")
    print(f"  {GRAY}Format:{RESET} {YELLOW}{fmt}{RESET}")
    print(f"  {GRAY}Folder:{RESET} {output_dir}")
    print()
    go = input(f"{WHITE}Start download? (y/n): {RESET}").strip().lower()
    if go != "y":
        print(f"{YELLOW}Cancelled.{RESET}")
        sys.exit(0)

    download(url, fmt, output_dir, audio_only, playlist_mode)

    again = input(f"\n{WHITE}Download another video? (y/n): {RESET}").strip().lower()
    if again == "y":
        main()
    else:
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Interrupted.{RESET}\n")