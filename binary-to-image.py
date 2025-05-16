""" Takes an input of binary data and image dimensions
    - > converting the binary to an 8-Bit RGB image
    Author: Finn McKinley
    Date: 16/05/2026
"""
# Library Imports
from PIL import Image
import time

PROGRAM_START_TIME = time.perf_counter() # Time starts when I say it does

def binary_only_input(raw_data=0):
    """ Takes user input of binary data and splits into 8 Bit chunks
        Returns the 8 Bit data as a list of 8 Bit strings 
    """
    function_start_time = time.perf_counter()
    try:
        if raw_data == 0:
            raw_data = str(input('Please input the raw binary data\n')) # Gets Input

        # Removes all non-binary data
        ones_and_zeros = str()
        for i in range(len(raw_data)):
            if raw_data[i] == '1' or raw_data[i] == '0':
                ones_and_zeros += raw_data[i]

        # Creates 8-Bit Packets
        eight_bit_data = []
        for i in range(0, len(ones_and_zeros) - (len(ones_and_zeros) % 8), 8):
            # print(ones_and_zeros[i: i + 8]) # DEBUG
            eight_bit_data.append(str(ones_and_zeros[i: i + 8]))

        ##### I HAVE DECIDED TO LEAVE THIS OUT AS THIS DATA IS LOST IN OTHER FUNCTIONS #####
        # Appends the leftovers to the 8-Bit
        # leftover = len(ones_and_zeros) % 8
        # if leftover != 0:
        #     eight_bit_data.append(ones_and_zeros[-leftover:])

    except UnboundLocalError:
        print("UnboundLocalError - Check the input isn't empty")
    except Exception as e:
        print(f'An error has occurred: {e}')
    else:
        print(f'Data recieved successfully | {len(eight_bit_data)} bytes')
        # print(eight_bit_data) # DEBUG
        end_time = time.perf_counter()
        elapsed = end_time - function_start_time
        print(f'binary_only_input time taken: {elapsed:.4f} s')
        return eight_bit_data

def text_file_to_binary(filepath):
    """ Takes a .txt file and returns it as a string of binary text """
    try:
        # Opens file
        with open(filepath, 'rb') as file:
            byte_data = file.read()
        
        binary_string =  ''.join(f'{byte:08b}' for byte in byte_data) # Converts to binary

        # print(f'Binary output\n{binary_string}') # DEBUG
        print('File converted to binary string')
        return binary_only_input(binary_string)

    except FileNotFoundError:
        print('File not found. Check the path and try again.')
    except Exception as e:
        print(f'An error has occurred: {e}')

def text_to_binary():
    try:
        raw_data = str(input('Please input the text you want converted\n')) # Gets Input

        binary_string =  ''
        for char in raw_data: 
            code_point = ord(char)
            if code_point > 255: # Checks the character can be converted
                raise ValueError(f'Character {repr(char)} cannot be encoded in 8-bit ASCII.')
            binary_string += f'{code_point:08b}' # Converts to binary

        # print(f'Binary output\n{binary_string}') # DEBUG
        return binary_only_input(binary_string)
    
    except ValueError as ve:
        print(f'ValueError: {ve}')
    except Exception as e:
        print(f'An error has occurred: {e}')

def binary_to_text(binary_strings):
    """ Takes a list of binary strings and converts it to text """
    text = ''.join(chr(int(string, 2)) for string in binary_strings)

    print(f'Text is:\n{text}') # DEBUG
    return text
        
def binary_to_grey_image(image_width, image_height, binary_data):
    """ Takes the image dimensions and binary data and creates an image file from it 
        image_width in pixels (integer)
        image_height in pixels (integer)
        binary_data as a list of 8-Bit binary data 
    """
    function_start_time = time.perf_counter()
    # Ensure correct amount of binary data
    pixel_count = image_width * image_height
    while len(binary_data) < pixel_count:
        binary_data.append('00000000')
    if len(binary_data) > pixel_count:
        binary_data = binary_data[0: pixel_count]
    
    byte_values = [int(b, 2) for b in binary_data] # [0-255] Grey scale values

    # Creates image
    image = Image.new('L', (image_width, image_height))
    image.putdata(byte_values)
    image.show()
    image.save('outputGrey.png')

    print('Success! Image created') # DEBUG
    end_time = time.perf_counter()
    elapsed = end_time - function_start_time
    print(f'binary_to_RGB time taken: {elapsed:.4f} s')
    print(f'{(len(binary_data) / 1_000_000) / (end_time - PROGRAM_START_TIME):.2f} MB/s')
    return 1 # Done!

def binary_to_RGB_image(image_width, image_height, binary_data):
    """ Takes the image dimensions and binary data and creates an image file from it 
        image_width in pixels (integer)
        image_height in pixels (integer)
        binary_data as a list of 8-Bit binary data 
    """
    function_start_time = time.perf_counter()

    # Ensure correct amount of binary data
    pixel_count = image_width * image_height
    while len(binary_data) < pixel_count * 3:
        binary_data.append('00000000')
    if len(binary_data) > pixel_count * 3:
        binary_data = binary_data[0: pixel_count * 3]
    
    pixel_values = [(int(c1, 2), int(c2, 2), int(c3, 2)) 
                    for c1, c2, c3 in zip(binary_data[::3], binary_data[1::3], binary_data[2::3])] # [0-255] Grey scale values
    print('Image data ready') # DEBUG

    # Creates image
    image = Image.new('RGB', (image_width, image_height))
    image.putdata(pixel_values)
    image.show()
    image.save('outputRGB.png')

    print('Success! Image created') # DEBUG
    end_time = time.perf_counter()
    elapsed = end_time - function_start_time
    print(f'binary_to_RGB time taken: {elapsed:.4f} s')
    print(f'{(len(binary_data) / 1_000_000) / (end_time - PROGRAM_START_TIME):.2f} MB/s')
    return 1 # Done!
    
def compare_data(input_data, output_data):
    """ Compares input_data against output_data for inconsistencies
        Files must be of same type and order 
    """
    correct_data = 0
    for i in range(len(output_data)):
        if input_data[i] == output_data[i]:
            correct_data += 1
    print(f'Data compared, {correct_data} correct datapoints vs {len(input_data)} datapoints -> {correct_data / len(input_data) * 100}% accurate')
    return 1 # Done!



# binary_strings = binary_only_input()
# text_file_to_binary('pi.txt')
# binary_to_text(binary_strings)
# text_to_binary()
# binary_to_grey_image(image_width=1024, image_height=1024, binary_data=text_file_to_binary('pi.txt'))
binary_to_RGB_image(image_width=2058, image_height=2058, binary_data=text_file_to_binary('Hamilton/shakespeare.txt'))

def test_against_pi():
    pi_binary = text_file_to_binary('pi.txt')
    output_pi = binary_to_text(pi_binary)
    with open('pi.txt', 'r') as file:
        real_pi = file.read()   
    compare_data(real_pi, output_pi)

# test_against_pi()

# END TIMER
# end_time = time.perf_counter()
# elapsed = end_time - PROGRAM_START_TIME
# print(f'Total program time taken: {elapsed:.4f} s')