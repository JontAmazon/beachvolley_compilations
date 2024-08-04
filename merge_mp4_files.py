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




#input_files = [
#    dirr + "/saved_output/20240803/all_highlights/highlights2.mp4",
#    dirr + "/saved_output/20240803/all_highlights/highlights3.mp4",
#    dirr + "/saved_output/20240803/all_highlights/highlights4.mp4",
#    dirr + "/saved_output/20240803/all_highlights/highlights5.mp4",
#    dirr + "/saved_output/20240803/all_highlights/highlights6.mp4",
#]

#input_files = [
    #dirr + "/saved_output/20240803/trimmed_set2.mp4", # 9:50
    #dirr + "/saved_output/20240803/trimmed_set3.mp4", # 9:00
    #dirr + "/saved_output/20240803/trimmed_set4.mp4", # 8:50
    #dirr + "/saved_output/20240803/trimmed_set5.mp4", # 10:50
    #dirr + "/saved_output/20240803/trimmed_set6.mp4", # 11:30
#]

#input_files = [
#    dirr + "/saved_output/20240803/mistakes_jonatan/mistakes_jonatan3.mp4",
#    dirr + "/saved_output/20240803/mistakes_jonatan/mistakes_jonatan4.mp4",
#    dirr + "/saved_output/20240803/mistakes_jonatan/mistakes_jonatan5.mp4",
#    dirr + "/saved_output/20240803/mistakes_jonatan/mistakes_jonatan6.mp4",
#]

#input_files = [
#    dirr + "/saved_output/20240803/mistakes_oskar/mistakes_oskar3.mp4",
#    dirr + "/saved_output/20240803/mistakes_oskar/mistakes_oskar4.mp4",
#    dirr + "/saved_output/20240803/mistakes_oskar/mistakes_oskar5.mp4",
#    dirr + "/saved_output/20240803/mistakes_oskar/mistakes_oskar6.mp4",
#]

#input_files = [
#    dirr + "/saved_output/20240803/mistakes_hakan/mistakes_hakan3.mp4",
#    dirr + "/saved_output/20240803/mistakes_hakan/mistakes_hakan4.mp4",
#    dirr + "/saved_output/20240803/mistakes_hakan/mistakes_hakan5.mp4",
#    dirr + "/saved_output/20240803/mistakes_hakan/mistakes_hakan6.mp4",
#]

input_files = [
    dirr + "/saved_output/20240803/mistakes_simon/mistakes_simon3.mp4",
    dirr + "/saved_output/20240803/mistakes_simon/mistakes_simon4.mp4",
    dirr + "/saved_output/20240803/mistakes_simon/mistakes_simon5.mp4",
    dirr + "/saved_output/20240803/mistakes_simon/mistakes_simon6.mp4",
]






create_compilation(input_files, output)

