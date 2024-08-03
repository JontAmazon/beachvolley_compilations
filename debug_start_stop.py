import os
import subprocess
import shutil
import time

ffmpeg_bin_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin"
os.chdir(ffmpeg_bin_path)


starts = [
14.345502138137817,
47.15669393539429,
66.64855194091797,
77.91318130493164,
104.28968048095703,
125.08669352531433,
179.14036798477173,
205.50090861320496,
236.740638256073,
275.52765798568726,
299.3586800098419,
313.5586793422699,
333.63857316970825,
367.1635956764221,
409.940701007843,
453.88744711875916,
472.33726239204407,
502.1933364868164,
529.8724536895752,
549.1464667320251,
580.9067530632019,
610.0220572948456,
633.6807250976562,
676.6934351921082,
695.1684436798096,
717.1598527431488,
746.5526506900787,
776.3406875133514,
810.7165670394897,
830.3217296600342,
887.7172031402588,
910.478627204895,
930.1166598796844,
952.2094519138336,
992.9335758686066,
1030.6671233177185,
1053.0,  # looks like this was missing
1076.2251770496368,
1101.7459099292755,
]

stops = [
32.93941354751587,
62.766632318496704,
75.36253452301025,
98.82355952262878,
117.19285368919373,
160.02044868469238,
193.12735772132874,
223.26357197761536,
254.07864665985107,
285.34056091308594,
309.62928438186646,
327.9519419670105,
344.98339200019836,
379.6223635673523,
422.4259924888611,
465.42620515823364,
481.5414414405823,
520.4685063362122,
539.822564125061,
571.466370344162,
591.2277462482452,
623.1485552787781,
645.7652254104614,
689.5096411705017,
707.8024470806122,
730.7205636501312,
759.0364348888397,
790.242495059967,
819.5774803161621,
847.6740393638611,
907.3552303314209,
922.3385462760925,
939.5381331443787,
963.7486050128937,
1003.75852227211,
1043.1134760379791,
1063.748510837555,
1093.887447834015,
1109.9884631633759,
]
#starts_and_stops = zip(starts, stops)
#for start_and_stop_tuple in starts_and_stops:
#    print(start_and_stop_tuple)

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
        print(f"extract_segment: {command=}")
        subprocess.run(command)  # ffmpeg -i {input_file} -ss {start} -to {end} -c copy
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

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"\n\nFolder '{folder_path}' and all its contents have been deleted.\n")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def seconds_to_timestamp(seconds):
    # Convert total seconds to hh:mm:ss format
    return time.strftime("%H:%M:%S", time.gmtime(seconds))




dirr = "C:/Users/jonat/Desktop/Code/trim_mp4/beach_compilations"
input_file = dirr + "/input/beach_20240714/20240714_game3.mp4"
segment_dir = dirr + "/segments"
output_dir = dirr + "/output"
delete_folder(output_dir)
os.makedirs(output_dir)

# Use ffmpeg to create segments and merge them together.
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
    print(f"\n creating beachvolley_trimmed.mp4 \n")
    create_compilation(segment_files, output)

