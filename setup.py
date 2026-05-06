import subprocess
import sys
import os
import webbrowser
import time
import pathlib
import platform
 
RED    = "\033[91m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
 
LOGO = f"""
{RED}██╗   ██╗{WHITE}████████╗{RED}██╗   ██╗██████╗ ███████╗
{RED}╚██╗ ██╔╝{WHITE}╚══██╔══╝{RED}██║   ██║██╔══██╗██╔════╝
{RED} ╚████╔╝ {WHITE}   ██║   {RED}██║   ██║██████╔╝█████╗
{RED}  ╚██╔╝  {WHITE}   ██║   {RED}██║   ██║██╔══██╗██╔══╝
{RED}   ██║   {WHITE}   ██║   {RED}╚██████╔╝██████╔╝███████╗
{RED}   ╚═╝   {WHITE}   ╚═╝   {RED} ╚═════╝ ╚═════╝ ╚══════╝
{GRAY}              Setup & Installation{RESET}
"""
 
SEP = f"{GRAY}{'─' * 58}{RESET}"
 
REQUIREMENTS = [
    "yt-dlp",
]
 
SENTINEL = pathlib.Path(__file__).parent / ".setup_done"

SOCIAL_URL = "https://guns.lol/dayzx"
 
 
def clear():
    os.system("cls" if os.name == "nt" else "clear")
 
 
def step(icon, msg, color=WHITE):
    print(f"  {color}{icon}  {WHITE}{msg}{RESET}")

def install_ffmpeg():
    system = platform.system()

    if system == "Linux":
        step("Checking ffmpeg...", "", CYAN)
        result = subprocess.run(["which", "ffmpeg"], capture_output=True)
        if result.returncode != 0:
            step("Installing ffmpeg via apt...", "", CYAN)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"])
            step("✔", "ffmpeg installed successfully", GREEN)
        else:
            step("✔", "ffmpeg already installed", GREEN)

    elif system == "Windows":
        step("Checking ffmpeg...", "", CYAN)
        result = subprocess.run(["where", "ffmpeg"], capture_output=True)
        if result.returncode != 0:
            step("Installing ffmpeg via winget...", "", CYAN)
            process = subprocess.Popen(
                ["winget", "install", "ffmpeg", "--silent"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in process.stdout:
                line = line.strip()
                if line:
                    print(f"  {GRAY}{line}{RESET}")
            process.wait()
            if process.returncode == 0:
                step("✔", "ffmpeg installed successfully", GREEN)
            else:
                step("⚠", "Could not auto-install ffmpeg.", YELLOW)
                print(f"\n  {YELLOW}Please install it manually:{RESET}")
                print(f"  {CYAN}https://ffmpeg.org/download.html{RESET}\n")
        else:
            step("✔", "ffmpeg already installed", GREEN)
 
 
def main():
    clear()
    print(LOGO)
    print(SEP)
    print(f"\n{BOLD}{WHITE}Installing dependencies…{RESET}\n")

    install_ffmpeg()
 
    all_ok = True
    for pkg in REQUIREMENTS:
        step(f"Installing {CYAN}{pkg}{RESET}…", CYAN)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--break-system-packages"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            step(f"{GREEN}{pkg}{WHITE}installed successfully", GREEN)
        else:
            step(f"{RED}Error for {pkg}:{RESET}\n{result.stderr.strip()}", RED)
            all_ok = False
        time.sleep(0.3)
 
    print(f"\n{SEP}")
 
    if all_ok:
        print(f"\n{GREEN}{BOLD}Done.{RESET}")
    else:
        print(f"\n{YELLOW}{BOLD}Some packages could not be installed.{RESET}")
 
    print(f"\n{SEP}")
    time.sleep(0.8)
    webbrowser.open(SOCIAL_URL)
 
    print(f"\n{SEP}")
    print(f"\n  {GRAY}You can now launch the downloader with:{RESET}")
    print(f"  {YELLOW}python YoutubeDownloader.py{RESET}\n")
    if all_ok:
     SENTINEL.write_text("ok")
 
    input(f"  {GRAY}Press Enter to exit…{RESET}")
 
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Cancelled.{RESET}\n")