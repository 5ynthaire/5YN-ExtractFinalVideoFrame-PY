import subprocess
import os
import sys

def get_video_info(video_path):
    """Get frame count and FPS using ffprobe."""
    # Frame count (video stream 0)
    cmd_frames = [
        'ffprobe', '-v', 'quiet', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', video_path
    ]
    result_frames = subprocess.run(cmd_frames, capture_output=True, text=True)
    if result_frames.returncode != 0:
        raise ValueError("Error getting frame count: " + result_frames.stderr)
    frame_count = int(result_frames.stdout.strip())
    
    # FPS (as fraction, e.g., '30/1')
    cmd_fps = [
        'ffprobe', '-v', 'quiet', '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', video_path
    ]
    result_fps = subprocess.run(cmd_fps, capture_output=True, text=True)
    if result_fps.returncode != 0:
        raise ValueError("Error getting FPS: " + result_fps.stderr)
    fps_str = result_fps.stdout.strip()
    fps = eval(fps_str)  # Safe for '30/1' -> 30.0; add error handling if needed
    
    return frame_count, fps

def extract_frame_by_index(video_path, output_path, target_frame_index):
    """Extract specific frame by index using select filter."""
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vf', f'select=eq(n\\,{target_frame_index})',
        '-vframes', '1', '-q:v', '1',  # High quality, one frame
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, check=True)
    if result.returncode != 0:
        raise ValueError("Extraction failed: " + result.stderr.decode())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python frame_extractor.py <video.mp4>")
        sys.exit(1)
    
    video = sys.argv[1]
    if not os.path.exists(video):
        print("Video not found!")
        sys.exit(1)
    
    output = video.replace('.mp4', '_last_frame.png')
    buffer_seconds = 0  # Adjustable: 0 for exact last frame, 2-3s buffer to avoid artifacts
    
    try:
        frame_count, fps = get_video_info(video)
        if frame_count == 0:
            raise ValueError("No frames in video!")
        
        buffer_frames = int(fps * buffer_seconds)
        target_frame = max(0, frame_count - buffer_frames - 1)  # -1 for 0-based indexing
        
        print(f"Video: {frame_count} frames at ~{fps} FPS")
        print(f"Targeting frame {target_frame} (buffer: {buffer_frames} frames / ~{buffer_seconds}s)")
        
        extract_frame_by_index(video, output, target_frame)
        print(f"Extracted frame {target_frame} to {output}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)