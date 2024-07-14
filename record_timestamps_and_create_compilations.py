import os
import subprocess
import shutil
import keyboard
import time

ffmpeg_bin_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin"
os.chdir(ffmpeg_bin_path)
# os.system("ffmpeg -version")

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and all its contents have been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def format_time(seconds):
    # Convert seconds into hh:mm:ss format
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def timestamp_to_seconds(timestamp):
    # Convert hh:mm:ss format to total seconds
    h, m, s = map(int, timestamp.split(':'))
    return h * 3600 + m * 60 + s

def seconds_to_timestamp(seconds):
    # Convert total seconds to hh:mm:ss format
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def generate_time_ranges(timestamps):
    time_ranges = []
    for timestamp in timestamps:
        start_seconds = timestamp_to_seconds(timestamp) - 8
        end_seconds = timestamp_to_seconds(timestamp) + 4
        if start_seconds < 0:
            start_seconds = 0  # Ensure start time does not go negative
        start_time = seconds_to_timestamp(start_seconds)
        end_time = seconds_to_timestamp(end_seconds)
        time_ranges.append((start_time, end_time))
    return time_ranges

def generate_highlight_time_ranges(timestamps):
    time_ranges = []
    for timestamp in timestamps:
        start_seconds = timestamp_to_seconds(timestamp) - 20  # should be enough
        end_seconds = timestamp_to_seconds(timestamp) + 2
        if start_seconds < 0:
            start_seconds = 0  # Ensure start time does not go negative
        start_time = seconds_to_timestamp(start_seconds)
        end_time = seconds_to_timestamp(end_seconds)
        time_ranges.append((start_time, end_time))
    return time_ranges

def record_timestamps():
    player1_timestamps = []
    player2_timestamps = []
    player3_timestamps = []
    player4_timestamps = []
    highlights_timestamps = []
    start_timestamps = [] # point is about to start
    stop_timestamps = []  # point ended
    print("Press '1' for Player 1, '2' for Player 2, etc, 'h' for a highlight, or '0' to quit.")
    print("Press 'j' for point is about to start, 'k' for point stopped.")

    starting_time = time.time()
    try:
        while True:
            if keyboard.is_pressed('1'):
                player1_timestamps.append(time.time() - starting_time)
                print(f"Player 1 timestamp recorded: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('2'):
                player2_timestamps.append(time.time() - starting_time)
                print(f"Player 2 timestamp recorded: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('3'):
                player3_timestamps.append(time.time() - starting_time)
                print(f"Player 3 timestamp recorded: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('4'):
                player4_timestamps.append(time.time() - starting_time)
                print(f"Player 4 timestamp recorded: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('h'): # highlight
                highlights_timestamps.append(time.time() - starting_time)
                print(f"Highlight timestamp: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('j'): # ball is about to start
                start_timestamps.append(time.time() - starting_time)
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('k'): # ball ends
                stop_timestamps.append(time.time() - starting_time)
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('0'):
                print("Exiting...")
                break
    except KeyboardInterrupt:
        pass

    # Convert Unix timestamps to hh:mm:ss format
    player1_timestamps = [format_time(ts) for ts in player1_timestamps]
    player2_timestamps = [format_time(ts) for ts in player2_timestamps]
    player3_timestamps = [format_time(ts) for ts in player3_timestamps]
    player4_timestamps = [format_time(ts) for ts in player4_timestamps]
    highlights_timestamps = [format_time(ts) for ts in highlights_timestamps]

    return (
        generate_time_ranges(player1_timestamps), # list of tuples (start, end)
        generate_time_ranges(player2_timestamps), # list of tuples (start, end)
        generate_time_ranges(player3_timestamps), # list of tuples (start, end)
        generate_time_ranges(player4_timestamps), # list of tuples (start, end)
        generate_highlight_time_ranges(highlights_timestamps), # list of tuples (start, end)
        start_timestamps, # list of strings (just start value)
        stop_timestamps,  # list of strings (just stop value) 
    )

def extract_segments(input_file, segments, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    segment_files = []
    for i, (start, end) in enumerate(segments):
        print(f"extracting segment {i+1}")
        output_file = os.path.join(output_dir, f"segment{i+1}.mp4")
        command = [
            "ffmpeg",
            "-i", input_file,
            "-ss", start,
            "-to", end,
            "-c", "copy",
            output_file
        ]
        subprocess.run(command)
        segment_files.append(output_file)
        print(f"Extracted segment {i+1}: {start} to {end}")
        print("\n\n\n")
    
    print("returning segment_files:")
    return segment_files

def create_compilation(segment_files, output_file):
    with open("file_list.txt", "w") as file_list:
        for segment_file in segment_files:
            file_list.write(f"file '{segment_file}'\n")
    
    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "file_list.txt",
        "-c", "copy",
        output_file
    ]
    subprocess.run(command)
    print(f"Compilation video created: {output_file}")
    os.remove("file_list.txt")



if __name__ == "__main__":
    dirr = "C:/Users/jonat/Desktop/Code/trim_mp4/beach_compilations"
    input_file = dirr + "/beachvolley.mp4"

    # 1. Semi automate generating timestamps
    p1, p2, p3, p4, highlights, starts, stops = record_timestamps()
    time_ranges_per_player = [p1, p2, p3, p4, highlights]
    print("\n\n Player 1 time ranges:")
    for start, end in p1:
        print(f"({start}, {end})")
    print("\n Player 2 time ranges:")
    for start, end in p2:
        print(f"({start}, {end})")
    print("\n Player 3 time ranges:")
    for start, end in p3:
        print(f"({start}, {end})")
    print("\n Player 4 time ranges:")
    for start, end in p4:
        print(f"({start}, {end})")
    print("\n Highlights time ranges:")
    for start, end in highlights:
        print(f"({start}, {end})")
    print("\n Points start:")
    for start in starts:
        print(f"{start}")
    print("\n Points stop:")
    for stop in stops:
        print(f"{stop}")

    # 2a. Use ffmpeg to create segments and merge them together, for each player
    segment_dir = dirr + "/segments"
    output_dir = dirr + "/output"
    delete_folder(output_dir)
    os.makedirs(output_dir)
    for i in range(4):
        print(f"\n\n Player {i+1}")
        delete_folder(segment_dir)
        output = output_dir + f"/compilation_player{i+1}.mp4"

        segments = time_ranges_per_player[i]
        segment_files = extract_segments(input_file, segments, segment_dir)
        print(f"\n create compilation for Player {i+1} \n")
        create_compilation(segment_files, output)

    # 2b. Same thing but for start and stop.
    print("Expecting len(starts) == len(stops)")
    print(f"len(starts): {len(starts)}")
    print(f"len(stops): {len(stops)}")
    if len(starts) != len(stops):
        for i in range(7):
            print(f"Something has gone wrong! len(starts) != len(stops)")
        print("\n Points start:")
        for start in starts:
            print(f"{start}")
        print("\n Points stop:")
        for stop in stops:
            print(f"{stop}")
    else:
        print(f"\n\n All points, but dead time trimmed away")
        delete_folder(segment_dir)
        output = output_dir + f"/beachvolley_trimmed.mp4"

        segments = list(zip(starts, stops))
        segment_files = extract_segments(input_file, segments, segment_dir)
        print(f"\n create beachvolley_trimmed.mp4 \n")
        create_compilation(segment_files, output)
