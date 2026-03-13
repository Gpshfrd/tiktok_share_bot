# TikTok Video Downloader Telegram Bot

A Telegram bot that allows users to quickly download TikTok videos directly inside Telegram.
The bot supports both **direct chat usage** and **inline mode**, making it easy to share videos in any conversation.

## Features

* Download TikTok videos by sending a link to the bot
* Inline mode: use the bot directly in any chat with `@tiktokvideosharebot <tiktok_url>`
* Automatic support for TikTok short links (`vt.tiktok.com`, `vm.tiktok.com`)
* Video caching using Telegram `file_id` for faster repeated downloads
* Simple deployment using Docker
* Persistent cache stored in a JSON file

## How It Works

1. A user sends a TikTok URL to the bot or invokes it inline in a chat.
2. The bot resolves short TikTok links and retrieves the direct video URL using an external API.
3. The video is sent to Telegram.
4. The bot stores the Telegram `file_id` of the video in a cache.
5. If the same video is requested again, the bot sends it instantly using the cached `file_id`.

This approach avoids downloading and storing large video files on the server while keeping responses fast.

## Usage

### Direct chat

Send a TikTok link to the bot:

```
https://www.tiktok.com/...
```

The bot will respond with the downloadable video.

### Inline mode

Use the bot directly in any chat:

```
@tiktokvideosharebot https://www.tiktok.com/...
```

Telegram will display a preview that can be sent to the chat.

## Tech Stack

* Python
* python-telegram-bot
* Docker
* TikTok video extraction API

## Notes

* The bot does not store video files locally.
* Only Telegram `file_id` values are cached for faster repeated responses.
* The cache persists between container restarts through a mounted volume.
