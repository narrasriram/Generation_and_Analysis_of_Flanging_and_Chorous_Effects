
# -*- coding: utf-8 -*-

# program: flanging_and_chorus_effect_generation.py
# author: Sriram Narra & Akhil Reddy Kallam
# course: CS 827
# date: December 08th 2018
# Final Project
# description: this program reads in a 
# filename.wav mono audio file and returns 
# the Modulated Effect signals wav files 
# -----------------------------------------


# Import required packages

import wave
from audioop import add
from audioop import mul

#-------------------------------------------
# function: source_wave
# purpose: reads the source file and returns 
# the data in the file
# parameter(s): <2> string (source_file_name),
#                   int frames
# return:  <2> _wave_params (parameters),
#              object (audio_data_bytes)

def source_wave(source_file_name, frames=10000000):
    with wave.open(source_file_name, 'rb') as wave_file:
        parameters= wave_file.getparams()
        audio_data_bytes = wave_file.readframes(frames)  
        if parameters.nchannels!=1:
            raise Exception("Stereo signals are not supported")
    return parameters, audio_data_bytes

#-------------------------------------------
# function: destination_wave
# purpose: writes the flanging effect file 
# data to output file
# parameter(s): <4> object (audio_data_bytes),
#                   _wave_params (parameters),
#                   string (outputfile), 
#                   string (outputfilenamesuffix)
    
def destination_wave(audio_data_bytes, parameters, outputfile, trailing_name):
    #dynamically format the filename by 
    #passing in data
    destination_file_name = outputfile.replace('.wav',
                        '_{}.wav'.format(trailing_name))
    with wave.open(destination_file_name,'wb') as wave_file:
        wave_file.setparams(parameters)
        wave_file.writeframes(audio_data_bytes)

# Write the source filepath and call the 
# source_wave function  

parameters, audio_data_bytes = source_wave(r'''filepath''')


#-------------------------------------------
# function: flanging_effect
# purpose: reads the input file and returns 
# the file content
# parameter(s): <4> object (audio_data_bytes),
#                   _wave_params (parameters),
#                   int (offset_milliseconds), 
#                   int (wet_factor)
# return:  object (audio_data_bytes)

def flanging_effect(audio_data_bytes, parameters, offset_milliseconds, wet_factor=1):

    #find the byte count which 
    #relates to the offset in
    #milliseconds
    offset_bytes= parameters.sampwidth * offset_milliseconds * int(parameters.framerate/1000)
    
    #Padding 0's corresponding to the delay duration
    start= b'\0'*offset_bytes
    
    #neglect the trailing part of delayed signal
    #to maintain the same length as source signal
    end= audio_data_bytes[:-offset_bytes]
    
    #applied the wet_factor
    multiplied_end= mul(audio_data_bytes[:-offset_bytes], parameters.sampwidth, wet_factor)
    return add(audio_data_bytes, start+ multiplied_end, parameters.sampwidth)

# Write the destination filepath and call the 
# destination_wave function  
destination_wave(flanging_effect(audio_data_bytes, parameters, offset_milliseconds=20, wet_factor=0.75),
            parameters, r'''filepath''', 'delay_20ms_0.75f')



#-------------------------------------------
# function: chorus_effect
# purpose: reads the input file and returns 
# the file content
# parameter(s): <4> object (audio_data_bytes),
#                   _wave_params (parameters),
#                   int (offset_milliseconds), 
#                   int (wet_factor)
# return:  object (audio_data_bytes)

def chorus_effect(audio_data_bytes, parameters, offset_milliseconds, wet_factor=1):

    #find the byte count which 
    #relates to the offset in
    #milliseconds
    offset_bytes= parameters.sampwidth * offset_milliseconds * int(parameters.framerate/1000)
    
    #Padding 0's corresponding to the delay duration
    start= b'\0'*offset_bytes
    
    #neglect the trailing part of delayed signal
    #to maintain the same length as source signal
    end= audio_data_bytes[:-offset_bytes]
    
    #applied the wet_factor
    multiplied_end= mul(audio_data_bytes[:-offset_bytes], parameters.sampwidth, wet_factor)
    return add(audio_data_bytes, start+ multiplied_end, parameters.sampwidth)

# Write the destination filepath and call the 
# destination_wave function  
destination_wave(chorus_effect(audio_data_bytes, parameters, offset_milliseconds=80, wet_factor=1),
            parameters, r'''filepath''', 'delay_80ms')


