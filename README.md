![5YN-ExtractFinalVideoFrame-PY](banner.png)

# Python Script: Extract Final Frames of Videos

## Purpose

This Python script extracts the last frame(s) from .mp4 videos. It supports an emerging workflow with the popularization of AI video generation, where users chain together videos by feeding the generating platform final frames.

## Requirements

- Python 3.6+
- ffmpeg installed and executable location added to PATH

## Commandline Switches

- `--all`: Extracts final frames from all videos in current directory. Warns if 20 > files.
- `--folder <folder_name>`: Specifies subfolder name to extact frames to. Creates if missing. Defaults to video's directory.
- `--frames`: Number of final frames to extract. Default 1.

## Usage

**Extract last frame of video.mp4**
`python frame_extractor.py video.mp4`

*Outputs: video_XXX.png in the same directory, where XXX is the 0-based frame index.*

**Extract last frame from all .mp4 videos in the current directory, outputting to subfolder my_outputs:**
`python frame_extractor.py --all --folder my_outputs`

**Extract last 3 frames from all .mp4 videos in the current directory, outputting to subfolder my_outputs:**
`python frame_extractor.py --all --frames 3 --folder my_outputs`

## Workflow Example

**Drag and Drop**

1. create extract_frame.bat in same location as frame_extractor.py:

```
python frame_extractor.py %1
```

2. Drag and drop video on to `extract_frame.bat`

## Code

View source: [frame_extractor.py](frame_extractor.py)

## License

This Python script is released under the [MIT License](LICENSE).

## About

**X**: [@5ynthaire](https://x.com/5ynthaire)  
**GitHub**: [https://github.com/5ynthaire](https://github.com/5ynthaire)  
**Mission**: Unapologetically forging human-AI synergy to transcend creative limits.  
**Attribution**: Created with Grok by xAI (no affiliation).
