import random
import subprocess
import os

inputname = input("Como se llama tu video: ")
with open("framesrate.bat", "w") as fr:
    fr.write("@echo OFF \nmediainfo --Output=\"Video;%%FrameCount%%\" " +str(inputname)+ " > framecount.txt"
"\nset /p Ftotal=<framecount.txt"
"\necho %Ftotal%"
"\nmediainfo --Output=\"Video;%%FrameRate%%\" " +str(inputname)+ " > frate.txt"
"\nset /p Frate=<frate.txt"
"\necho %Frate%")
subprocess.run(["framesrate.bat"])
fr.close()
os.remove('framesrate.bat')
os.system('cls')

f = open("randomize.bat","w")
f.write("mkdir frames\n")

with open("framecount.txt", "r") as framecount:
    frames = int(framecount.readlines()[0])
    framecount.close()
    os.remove('framecount.txt')

with open("frate.txt", "r") as frate:
    framerate = float(frate.readlines()[0])
    frate.close()
    os.remove('frate.txt')

duracion = frames / framerate

list = open("list.txt","w")
for i in range(1, frames):
    list.write("file 'frames\out"+str(i)+".mp4'\n")
list.close()

lines = open('list.txt').readlines()
random.shuffle(lines)
open('list.txt', 'w').writelines(lines)

for i in range(1, frames): 
    f.write("ffmpeg -ss "+str(i/framerate)+" -t " +str(1/framerate)+ " -i " +str(inputname)+ " -vcodec h264 -acodec aac \"frames\out"+str(i)+".mp4\"\n")
    if i == frames:
        break
    f.close

f = open("randomize.bat","a")
f.write("\nffmpeg -t " +str(round(duracion,2))+ " -f concat -safe 0 -i list.txt -vcodec h264 -acodec aac -crf 27 outputfinal.mp4")
f.write("\ndel list.txt")
f.write("\nrmdir /s /q frames")
f.write("\ndel randomize.bat")
f.close()

subprocess.run(["randomize.bat"])

os.system('cls')
print("Video randomizado :D")


