import glob
import subprocess


f = open('finished.txt','r')
f_line = f.readline()
while f_line:
	f_line = f_line.strip()
	cmd = "rm gend_data/" + str(f_line)
	subprocess.call(cmd, shell=True)
	f_line = f.readline()
f.close()