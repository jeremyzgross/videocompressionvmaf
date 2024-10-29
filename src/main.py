#goal is to analazyze a file, get to a target vmaf result that is over 90 and compress to the smallest size possible while still being over 70
# select file path
#saves to variable
# function runs file through compression with crf value. Another function runs vmaf on the output file.
#NEED to print "VMAF score"
# if vmaf is under 90, it compresses again with a lower crf value. Keep looping until vmaf is over 90. Start with crf value of 20 and go down until vmaf is over 90.
# once vmaf is over 90, save the file with the crf value that got it over 90. 
#print the vmaf value and crf value


import os 
import subprocess
import tkinter
import tkinter.filedialog

#output_files directory
output_files_dir = "/Users/jeremyzgross/videocompressionvmaf/output_files"

#select file path
file_chosen = tkinter.filedialog.askopenfilename(title="Select a file")
#print(file_chosen)


def analyze_file(file_path):
  ideal_vmaf_score = False
  crf_value = 40
  file_name, file_extension = os.path.splitext(os.path.basename(file_path))
  output_files_name = f"{file_name}_output_{crf_value}{file_extension}"
  full_output_path = os.path.join(output_files_dir, output_files_name)
  raw_ffmpeg_cmd_line = f"ffmpeg -i {file_path} -c:v libx264 -crf {crf_value} -preset fast -y {full_output_path}"
  subprocess.run(raw_ffmpeg_cmd_line, shell=True)

  while not ideal_vmaf_score:
    vmaf_cmd = f"ffmpeg -i {file_path} -i {full_output_path} -lavfi libvmaf -f null -"
    subprocess.run(vmaf_cmd, shell=True)
    vmaf_output = subprocess.check_output(vmaf_cmd, shell=True, stderr=subprocess.STDOUT).decode()
    vmaf_score = 0

    for line in vmaf_output.split('\n'):
      if "VMAF score:" in line:
        vmaf_score = float(line.split(":")[-1].strip())
        print(f"VMAF score HERE: {vmaf_score}")
    os.remove(full_output_path)

    if vmaf_score < 80:
      crf_value -= 1
      output_files_name = f"{file_name}_output_{crf_value}{file_extension}"
      full_output_path = os.path.join(output_files_dir, output_files_name)
      raw_ffmpeg_cmd_line = f"ffmpeg -i {file_path} -c:v libx264 -crf {crf_value} -preset fast -y {full_output_path}"
      subprocess.run(raw_ffmpeg_cmd_line, shell=True)
    else:
      ideal_vmaf_score = True
      print(f"Final VMAF score: {vmaf_score}, Final CRF value: {crf_value}")


analyze_file(file_chosen)

