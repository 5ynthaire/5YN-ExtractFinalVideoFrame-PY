# Extract Final Frame of Video

## Purpose

This Python script for extracts the final frame of videos, an emerging workflow with the advent of AI video generation where users chain together videos by feeding the generating platform the final frames.

## Requirements

- Python 3.6+
- ffmpeg installed to PATH

## Usage

`python frame_extractor.py video.mp4`

## Workflow Example

**Drag and Drop**

extract_frame.bat:

```
python frame_extractor.py %1
```

## Commandline Switches

- `--all`: Extracts final frames from all videos in working directory
- `--folder folder_name`: Specifies subfolder name to extact frames to
- `--buffer seconds`: 

## Code

View source: [frame_extractor.py](frame_extractor.py)

## License

This Python script is released under the [MIT License](LICENSE).

## About

**X**: [@5ynthaire](https://x.com/5ynthaire)  
**GitHub**: [https://github.com/5ynthaire](https://github.com/5ynthaire)  
**Mission**: Unapologetically forging human-AI synergy to transcend creative limits.  
**Attribution**: Created with Grok by xAI (no affiliation).
