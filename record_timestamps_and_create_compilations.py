import os
import subprocess
import shutil
import keyboard
import time

ffmpeg_bin_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin"
ffmpeg_exe = os.path.join(ffmpeg_bin_path, "ffmpeg.exe")
if not os.path.isfile(ffmpeg_exe):
    ffmpeg_exe = "ffmpeg"

def print_red(text):
    print(f"\033[91m{text}\033[0m")

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"\n\nFolder '{folder_path}' and all its contents have been deleted.\n")
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
        end_seconds = timestamp_to_seconds(timestamp) + 2
        if start_seconds < 0:
            start_seconds = 0  # Ensure start time does not go negative
        start_time = seconds_to_timestamp(start_seconds)
        end_time = seconds_to_timestamp(end_seconds)
        time_ranges.append((start_time, end_time))
    return time_ranges

def generate_highlight_time_ranges(timestamps, highlight_length):
    time_ranges = []
    for timestamp in timestamps:
        start_seconds = timestamp_to_seconds(timestamp) - highlight_length  # 10, 16, 22
        end_seconds = timestamp_to_seconds(timestamp) + 0
        if start_seconds < 0:
            start_seconds = 0  # Ensure start time does not go negative
        start_time = seconds_to_timestamp(start_seconds)
        end_time = seconds_to_timestamp(end_seconds)
        time_ranges.append((start_time, end_time))
    return time_ranges

def record_timestamps():
    player1_mistakes = [] # player 1 does a mistake
    player2_mistakes = []
    player3_mistakes = []
    player4_mistakes = []
    player1_timestamps = [] # player 1 receives serve
    player2_timestamps = []
    player3_timestamps = []
    player4_timestamps = []
    highlights_timestamps1 = [] # 10 sec long highlights end
    highlights_timestamps2 = [] # 16 sec long highlights end
    highlights_timestamps3 = [] # 22 sec long highlights end
    highlights_timestamps4 = [] # 30 sec long highlights end
    start_timestamps = [] # point is about to start
    stop_timestamps = []  # point ended

    def verify_starts_and_stops():
        """Make sure I don't forget start or stop."""
        if len(start_timestamps) > len(stop_timestamps) + 1:
            for _ in range(10):
                print_red("Too many start times. Removing last one.")
            del start_timestamps[-1]
        if len(start_timestamps) < len(stop_timestamps):
            for _ in range(10):
                print_red("Too many stop times. Removing last one.")
            del stop_timestamps[-1]

    print_red("Friendly reminder: changed to correct input video in the code?")
    print("Press 'j' for point starts, 'k' for point stopped.")
    print("Press '5' for Player 1 serve reception, '6' for Player 2, etc.")
    print("Press '1' for Player 1 mistake , '2' for Player 2, etc.")
    print("Press 'h' for 10 sec highlight, 'g' for 16 sec, 'f' for 22 sec, 'd' for 30 sec")
    print("Press '0' to quit.")

    starting_time = time.time()
    try:
        while True:
            if keyboard.is_pressed('1'):
                player1_mistakes.append(time.time() - starting_time)
                print(f"Player 1 mistake: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('2'):
                player2_mistakes.append(time.time() - starting_time)
                print(f"Player 2 mistake: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('3'):
                player3_mistakes.append(time.time() - starting_time)
                print(f"Player 3 mistake: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('4'):
                player4_mistakes.append(time.time() - starting_time)
                print(f"Player 4 mistake: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time

            elif keyboard.is_pressed('5'):
                player1_timestamps.append(time.time() - starting_time)
                print(f"Player 1: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('6'):
                player2_timestamps.append(time.time() - starting_time)
                print(f"Player 2: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('7'):
                player3_timestamps.append(time.time() - starting_time)
                print(f"Player 3: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('8'):
                player4_timestamps.append(time.time() - starting_time)
                print(f"Player 4: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time

            elif keyboard.is_pressed('h'): # 10 sec highlight
                highlights_timestamps1.append(time.time() - starting_time)
                print(f"Highlight: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('g'): # 16 sec highlight
                highlights_timestamps2.append(time.time() - starting_time)
                print(f"Highlight: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('f'): # 22 sec highlight
                highlights_timestamps3.append(time.time() - starting_time)
                print(f"Highlight: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
            elif keyboard.is_pressed('d'): # 30 sec highlight
                highlights_timestamps4.append(time.time() - starting_time)
                print(f"Highlight: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time

            elif keyboard.is_pressed('j'): # ball is about to start
                start_timestamps.append(time.time() - starting_time - 2 - 2 - 4) # 2s before the serve, 2s to start of video after starting script, 4s more required in my experience
                print(f"\nPoint starts: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
                verify_starts_and_stops()
            elif keyboard.is_pressed('k'): # ball ends
                stop_timestamps.append(time.time() - starting_time - 2) # count with 2 seconds to start of video after starting script
                print(f"Point ended: {time.time() - starting_time}")
                time.sleep(0.2)  # debounce time
                verify_starts_and_stops()
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
    player1_mistakes = [format_time(ts) for ts in player1_mistakes]
    player2_mistakes = [format_time(ts) for ts in player2_mistakes]
    player3_mistakes = [format_time(ts) for ts in player3_mistakes]
    player4_mistakes = [format_time(ts) for ts in player4_mistakes]
    highlights_timestamps1 = [format_time(ts) for ts in highlights_timestamps1]
    highlights_timestamps2 = [format_time(ts) for ts in highlights_timestamps2]
    highlights_timestamps3 = [format_time(ts) for ts in highlights_timestamps3]
    highlights_timestamps4 = [format_time(ts) for ts in highlights_timestamps4]

    # merge all highlights. (wops, ugly code).
    all_highlights = []
    h1 = generate_highlight_time_ranges(highlights_timestamps1, 10),
    h2 = generate_highlight_time_ranges(highlights_timestamps2, 16),
    h3 = generate_highlight_time_ranges(highlights_timestamps3, 22),
    h4 = generate_highlight_time_ranges(highlights_timestamps4, 30),
    if len(h1) > 0:
        h1 = h1[0] # list of tuples (start, end)
    if len(h2) > 0:
        h2 = h2[0] # list of tuples (start, end)
    if len(h3) > 0:
        h3 = h3[0] # list of tuples (start, end)
    if len(h4) > 0:
        h4 = h4[0] # list of tuples (start, end)
    if len(h1) > 0:
        all_highlights = all_highlights + h1
    if len(h2) > 0:
        all_highlights = all_highlights + h2
    if len(h3) > 0:
        all_highlights = all_highlights + h3
    if len(h4) > 0:
        all_highlights = all_highlights + h4

    return (
        generate_time_ranges(player1_timestamps), # list of tuples (start, end)
        generate_time_ranges(player2_timestamps), # list of tuples (start, end)
        generate_time_ranges(player3_timestamps), # list of tuples (start, end)
        generate_time_ranges(player4_timestamps), # list of tuples (start, end)
        generate_time_ranges(player1_mistakes), # list of tuples (start, end)
        generate_time_ranges(player2_mistakes), # list of tuples (start, end)
        generate_time_ranges(player3_mistakes), # list of tuples (start, end)
        generate_time_ranges(player4_mistakes), # list of tuples (start, end)
        all_highlights,                           # list of tuples (start, end)
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
            ffmpeg_exe,
            "-i", input_file,
            "-ss", start,
            "-to", end,
            "-c", "copy",
            output_file
        ]
        print(f"extract_segment: {command=}")
        subprocess.run(command, check=True)  # ffmpeg -i {input_file} -ss {start} -to {end} -c copy
        segment_files.append(output_file)
        print(f"Extracted segment {i+1}: {start} to {end}")
        print("\n\n\n")
    print("returning segment_files:")
    return segment_files

def create_compilation(segment_files, output_file):
    if not segment_files:
        print_red(f"Skipping compilation, no segments found for: {output_file}")
        return False

    file_list_path = os.path.join(os.path.dirname(output_file), "file_list.txt")
    with open(file_list_path, "w", encoding="utf-8") as file_list:
        for segment_file in segment_files:
            # ffmpeg concat demuxer expects paths in a plain text list.
            normalized = segment_file.replace("\\", "/").replace("'", "'\\''")
            file_list.write(f"file '{normalized}'\n")
    
    command = [
        ffmpeg_exe,
        "-f", "concat",
        "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",
        output_file
    ]
    subprocess.run(command, check=True)
    print(f"Compilation video created: {output_file}")
    os.remove(file_list_path)
    return True






if __name__ == "__main__":
    dirr = os.path.dirname(os.path.abspath(__file__))
    input_file = dirr + "/input/indoor/2026.02.14-div3-vs-vindrarp-set4.mp4"

    # 1. Semi automate generating timestamps
    p1, p2, p3, p4, m1, m2, m3, m4, highlights, starts, stops = record_timestamps()
    time_ranges_per_player = [p1, p2, p3, p4, highlights]  # including highlights here as well, even
    time_ranges_per_player_mistakes = [m1, m2, m3, m4]     # though highlights are not player specific >:)

    def print_all_time_ranges():
        """Print all time ranges (for the video segments)."""
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
        print("\n\n Player 1 mistakes time ranges:")
        for start, end in m1:
            print(f"({start}, {end})")
        print("\n\n Player 2 mistakes time ranges:")
        for start, end in m2:
            print(f"({start}, {end})")
        print("\n\n Player 3 mistakes time ranges:")
        for start, end in m3:
            print(f"({start}, {end})")
        print("\n\n Player 4 mistakes time ranges:")
        for start, end in m4:
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
    print_all_time_ranges()

    segment_dir = dirr + "/segments"
    output_dir = dirr + "/output"
    delete_folder(output_dir)
    os.makedirs(output_dir)

    # 2a. For each player, use ffmpeg to create segments and merge them together.

    # serve reception for each player:    
    for i in range(5):
        print("\n\n")
        for j in range(3):
            print_red(f"\tPlayer {i+1} serve receptions")
        delete_folder(segment_dir)
        if i == 4:
            output = output_dir + f"/highlights.mp4" # include highlights here as well, hehe >:)
        else:
            output = output_dir + f"/recep_player{i+1}.mp4"

        segments = time_ranges_per_player[i]
        segment_files = extract_segments(input_file, segments, segment_dir)
        print_red(f"\n creating serve reception compilation for Player {i+1} \n")
        create_compilation(segment_files, output)

    # mistakes for each player:
    for i in range(4):
        print("\n\n")
        for j in range(3):
            print_red(f"\tPlayer {i+1} mistakes")
        delete_folder(segment_dir)
        output = output_dir + f"/mistakes_player{i+1}.mp4"

        segments = time_ranges_per_player_mistakes[i]
        segment_files = extract_segments(input_file, segments, segment_dir)
        print_red(f"\n creating fail compilation for Player {i+1} \n")
        create_compilation(segment_files, output)

    # 2b. Use ffmpeg to create segments annd merge them together, for all start and stop times.
    print("\n\n")
    for i in range(3):
        print(f"\tVideo with ALL points, but dead time trimmed away")
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
        delete_folder(segment_dir)
        output = output_dir + f"/beachvolley_trimmed.mp4"
        
        # test fix script:
        new_starts, new_stops = [], []
        for start in starts:
            new_starts.append(seconds_to_timestamp(start))
        starts = new_starts
        for stop in stops:
            new_stops.append(seconds_to_timestamp(stop))
        stops = new_stops

        segments = list(zip(starts, stops))
        print(f"{segments=}")
        print(f"{segment_dir=}")
        segment_files = extract_segments(input_file, segments, segment_dir)

        for _ in range(5):
            print_red("this is how segment_files looks:")
        print(segment_files)
        print(type(segment_files))

        print_red(f"\n creating beachvolley_trimmed.mp4 \n")
        create_compilation(segment_files, output)
    
    print_all_time_ranges()
