import os
import subprocess
import shutil

ffmpeg_bin_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin"
os.chdir(ffmpeg_bin_path)

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"\n\nFolder '{folder_path}' and all its contents have been deleted.\n")
    else:
        print(f"Folder '{folder_path}' does not exist.")

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

dirr = "C:/Users/jonat/Desktop/Code/trim_mp4/beach_compilations"
output_dir = dirr + "/output"
delete_folder(output_dir)
os.makedirs(output_dir)
output = dirr + "/output/concat_video.mp4"




input_files = [
    dirr + "/saved_output/20240714/all_highlights/highlights_game3.mp4",
    dirr + "/saved_output/20240714/all_highlights/highlights_game2_missed_serves_but_good_enough.mp4",
    dirr + "/saved_output/20240714/all_highlights/highlights_game1_missed_ends.mp4",
]


create_compilation(input_files, output)

