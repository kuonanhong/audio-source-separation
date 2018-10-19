import librosa
import numpy as np 
#import mathplotlib.pyplot as plt 
import os
import re

path= "../DSD100subset/" 
path_mixtures = path + "Mixtures/Dev/"
path_sources = path + "Sources/Dev/"
destination_path = "../Processed/Mixtures"
phase_path= "../Processed/Phases"
bass_path="../Processed/Bass"
vocals_path="../Processed/Vocals"
drums_path="../Processed/Drums"
others_path="../Processed/Others"
source_dest_paths=[vocals_path,bass_path,drums_path,others_path]
def process(file_path,direc,destination_path,phase_bool):
	t1,t2=librosa.load(file_path,sr=None)
	duration=librosa.get_duration(t1,t2)
	regex = re.compile(r'\d+')
	index=regex.findall(direc)
	#print(index)
	for start in range(0,int(duration//20)):
		wave_array, fs = librosa.load(file_path,sr=None,offset=start*20.0,duration =20.0)
		mag, phase = librosa.magphase(librosa.stft(wave_array, n_fft=1024,hop_length=256,window='hann',center='True'))
		if not os.path.exists(destination_path):
			os.makedirs(destination_path)
		np.save(os.path.join(destination_path,(index[0] +"_" + str(start) +'_m.npy')),mag)
		if phase_bool:
			if not os.path.exists(phase_path):
				os.makedirs(phase_path)
			np.save(os.path.join(phase_path,(index[0]+"_" +str(start)+'_p.npy')),phase)
	return	




for subdirs, dirs, files in os.walk(path_mixtures):
	for direc in dirs:
		print('working with '+ direc)
		for s,d,f in os.walk(path_mixtures + direc):
			
			process(os.path.join(path_mixtures,direc,f[0]),direc,destination_path,True)
			
for subdirs, dirs, files in os.walk(path_sources):
	for direc in dirs:
		print('source with '+ direc)
		for s,d,file in os.walk(path_sources + direc):
			for i in range(0,4):
				print(file[i])
				process(os.path.join(path_sources,direc,file[i]),direc,source_dest_paths[i],False)
				
					
