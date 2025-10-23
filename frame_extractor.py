import subprocess
import os
import sys
import argparse
import glob

def get_video_info(video_path):
    """Get frame count and FPS using ffprobe."""
    # Frame count (video stream 0)
    cmd_frames = [
        'ffprobe', '-v', 'quiet', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', video_path
    ]
    result_frames = subprocess.run(cmd_frames, capture_output=True, text=True)
    if result_frames.returncode != 0:
        raise ValueError(f"Error getting frame count: {result_frames.stderr.strip()}")
    frame_count = int(result_frames.stdout.strip())
    
    # FPS (as fraction, e.g., '30/1')
    cmd_fps = [
        'ffprobe', '-v', 'quiet', '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', video_path
    ]
    result_fps = subprocess.run(cmd_fps, capture_output=True, text=True)
    if result_fps.returncode != 0:
        raise ValueError(f"Error getting FPS: {result_fps.stderr.strip()}")
    fps_str = result_fps.stdout.strip()
    try:
        fps = eval(fps_str)  # Safe for '30/1' -> 30.0
    except:
        raise ValueError(f"Invalid FPS format: {fps_str}")
    
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
        raise ValueError(f"Extraction failed: {result.stderr.decode().strip()}")

def unique_filename(path):
    """Generate unique filename if it exists, appending _1, _2, etc."""
    if not os.path.exists(path):
        return path
    
    dir_name, fname = os.path.split(path)
    name, ext = os.path.splitext(fname)
    counter = 1
    while True:
        new_name = f"{name}_{counter}{ext}"
        new_path = os.path.join(dir_name, new_name)
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def process_video(video_path, output_dir, num_frames=1):
    """Process a single video: extract last N frames and save to output_dir."""
    if not os.path.exists(video_path):
        print(f"Error: Video '{video_path}' not found!")
        return
    
    # Generate base output filename
    base_name = os.path.splitext(os.path.basename(video_path))[0]  # e.g., 'morph_seg1' from 'morph_seg1.mp4'
    
    try:
        frame_count, fps = get_video_info(video_path)
        if frame_count == 0:
            raise ValueError("No frames detected in video!")
        
        if num_frames > frame_count:
            print(f"Warning: Requested {num_frames} frames, but video has only {frame_count}. Extracting all.")
            num_frames = frame_count
        
        start_frame = frame_count - num_frames  # 0-based start index for last N
        target_frames = list(range(max(0, start_frame), frame_count))
        
        print(f"Video: {video_path}")
        print(f"  {frame_count} frames at ~{fps:.1f} FPS")
        print(f"  Extracting last {num_frames} frames: {target_frames}")
        
        extracted_count = 0
        for target_frame in target_frames:
            # Format frame number: 3-digit zero-pad if <1000, full otherwise
            frame_str = f"{target_frame:03d}" if target_frame < 1000 else str(target_frame)
            tentative_output = os.path.join(output_dir, f"{base_name}_{frame_str}.png")
            
            # Ensure unique
            output = unique_filename(tentative_output)
            
            print(f"    Frame {target_frame}: {output}")
            extract_frame_by_index(video_path, output, target_frame)
            extracted_count += 1
        
        print(f"  Done! {extracted_count} frames extracted successfully.\n")
    except Exception as e:
        print(f"Error processing {video_path}: {e}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract last N frames from video(s) for AI chaining. Supports single file or all videos in folder.")
    parser.add_argument("video", nargs='?', help="Path to input video file (e.g., video.mp4). Omit for --all mode.")
    parser.add_argument("--frames", type=int, default=1, help="Number of last frames to extract (default: 1)")
    parser.add_argument("--all", action='store_true', help="Process ALL .mp4 videos in current folder. Warns if >20.")
    parser.add_argument("--folder", type=str, help="Output folder (creates if missing). Defaults to video dir or current.")
    args = parser.parse_args()
    
    num_frames = args.frames
    if num_frames < 1:
        print("Error: --frames must be at least 1.")
        sys.exit(1)
    
    # Validate modes
    if args.all and args.video:
        print("Error: Use either a single video or --all, not both.")
        sys.exit(1)
    if not args.all and not args.video:
        print("Error: Specify a video file or use --all.")
        sys.exit(1)
    
    # Set output dir
    output_dir = args.folder
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    elif args.video:
        output_dir = os.path.dirname(args.video) or '.'
    else:  # --all
        output_dir = args.folder or '.'
        os.makedirs(output_dir, exist_ok=True)
    
    # Single video mode
    if not args.all:
        process_video(args.video, output_dir, num_frames)
    
    # --all mode
    else:
        video_pattern = os.path.join('.', '*.mp4')  # Add more extensions if needed: + ['*.mov', '*.avi']
        videos = glob.glob(video_pattern)
        if not videos:
            print("No .mp4 videos found in current folder.")
            sys.exit(0)
        
        print(f"Found {len(videos)} .mp4 video(s) in current folder.")
        if len(videos) > 20:
            response = input("Warning: More than 20 videos. Continue? (y/N): ").strip().lower()
            if response != 'y':
                print("Aborted.")
                sys.exit(0)
        
        print(f"\nProcessing {len(videos)} videos, extracting last {num_frames} frame(s) each...\n")
        for video in sorted(videos):  # Alphabetical order for consistency
            process_video(video, output_dir, num_frames)
        print("All videos processed!")
