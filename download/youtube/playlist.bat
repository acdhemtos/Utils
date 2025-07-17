@echo off
setlocal enabledelayedexpansion

:: Download Youtube Playlist in Best Video+Audio

:: Check if folder path is passed
if "%~1"=="" (
 echo Usage: download_playlist.bat "C:\path\to\folder" [playlist_url]
 exit /b 1
)

:: Check if playlist URL is passed
if "%~2"=="" (
 echo Please provide the playlist URL.
 exit /b 1
)

:: Get folder and URL
set "TARGET_FOLDER=%~1"
set "PLAYLIST_URL=%~2"

:: Create target folder if it doesn't exist
if not exist "%TARGET_FOLDER%" (
 mkdir "%TARGET_FOLDER%"
)

:: Download using yt-dlp
yt-dlp ^
 --yes-playlist ^
 -f "bv*+ba/b" ^
 --merge-output-format mp4 ^
 --output "%TARGET_FOLDER%\%%(playlist_index)02d) %%(title)s.%%(ext)s" ^
 "%PLAYLIST_URL%"

echo Done downloading to "%TARGET_FOLDER%"
