
import os
import time
import subprocess
import pathlib
from shutil import copyfile


# author: peter-426

# https://docs.python.org/3/library/subprocess.html
# subprocess.run waits for the process to end

# https://www.techrepublic.com/article/how-to-use-secure-copy-with-ssh-key-authentication/
# https://www.digitalocean.com/community/tutorials/how-to-use-sftp-to-securely-transfer-files-with-a-remote-server

# https://raspi.tv/2012/how-to-create-a-new-user-on-raspberry-pi
# https://www.jaredwolff.com/passwordless-ssh-raspberry-pi/#passwordless-login


testing=0

######################################################################  
csv_filename = "colony_centers.csv"

r_pi_IP = "172.20.122.232"  # change this IP!

raspberry_pi_path = "pi@"+r_pi_IP+":/home/pi/camera-code/MF-Camera/python/"

raspberry_pi_csv_file = raspberry_pi_path+csv_filename

OT_IP   = "169.254.16.106"  # change this IP!

dest_folder_OT = "root@"+OT_IP+":/data/user_storage"  
########################################################################

prev_mtime = 0
curr_mtime=0

wait_time=5

# localtime = time.localtime()
# result = time.strftime("%I:%M:%S %p", localtime)
# print("time is :", result, "\n\n")

fname = pathlib.Path(csv_filename)
file_stat = fname.stat()
prev_mtime=file_stat.st_mtime


devnull = open(os.devnull, 'w')


while 1:

    while 1: 
        temp=subprocess.run( ["scp","-p", raspberry_pi_csv_file, "."], stdout=devnull)
        
        #print("get csv_file: ", temp.stdout, temp.stderr, temp.returncode)

        fname = pathlib.Path(csv_filename);
        file_stat = fname.stat();
        curr_mtime=file_stat.st_mtime;
        
        if temp.returncode == 0:
            with open(csv_filename, 'r') as f:              
                if prev_mtime < curr_mtime:
                    print("image mtime: prev=%s, curr=%s" % (prev_mtime, curr_mtime))
                    prev_mtime = curr_mtime
                    break
                else:
                    time.sleep(wait_time) # seconds
    
    copyfile(csv_filename, "colony_centers_OT.csv")
    
    if testing == 1:
        print("put colony_center.csv to OT") 
    else:
        # note: run() expects a list of args
        temp=subprocess.run( ["scp", "-i", "ot2_ssh_key", "./colony_centers_OT.csv", dest_folder_OT])
        print("put to OT: ", temp.stdout, temp.stderr, temp.returncode)


# args = ["ping", "www.yahoo.com"]
# process = subprocess.Popen(args, stdout=subprocess.PIPE)

# data = process.communicate()
# for line in data:
#     print(line)

