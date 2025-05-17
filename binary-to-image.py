""" Takes an input of binary data and image dimensions
    - > converting the binary to an 8-Bit RGB image
    Author: Finn McKinley
    Date: 16/05/2026
"""
# Library Imports
from PIL import Image
import time
import os

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
        print(f'binary_only_input time taken: {elapsed:.4f} s\n')
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
        
def binary_to_grey_image(image_width, image_height, binary_data, image_name='outputGrey.png'):
    """ Takes the image dimensions and binary data and creates an image file from it 
        image_width in pixels (integer)
        image_height in pixels (integer)
        binary_data as a list of 8-Bit binary data 
    """
    function_start_time = time.perf_counter()
    # Ensure correct amount of binary data
    pixel_count = image_width * image_height

    data_length = len(binary_data) * 8 # Length in bits
    header = f'{data_length:032b}' # 32-bit string header
    header_chunks = [header[i: i + 8] for i in range(0, 32, 8)] # Converts 32-bit string to 8-bit chunks

    binary_data = header_chunks + binary_data # Appends header to the start of the binary data

    while len(binary_data) < pixel_count:
        binary_data.append('00000000')
    if len(binary_data) > pixel_count:
        binary_data = binary_data[0: pixel_count]
    
    byte_values = [int(b, 2) for b in binary_data] # [0-255] Grey scale values

    # Creates image
    image = Image.new('L', (image_width, image_height))
    image.putdata(byte_values)
    image.show()
    image.save(image_name)

    print('Success! Image created') # DEBUG
    end_time = time.perf_counter()
    elapsed = end_time - function_start_time
    data_size = len(binary_data) / (1024 ** 2)
    print(f'{data_size:.4f} MB of data converted to images in {elapsed:.4f} s')
    print(f'Data processed at {data_size / elapsed:.4f} MB/s\n')
    return 1 # Done!

def binary_to_RGB_image(image_width, image_height, binary_data, image_name='outputRGB.png'):
    """ Takes the image dimensions and binary data and creates an image file from it 
        image_width in pixels (integer)
        image_height in pixels (integer)
        binary_data as a list of 8-Bit binary data 
    """
    function_start_time = time.perf_counter()

    # Ensure correct amount of binary data
    pixel_count = image_width * image_height

    data_length = len(binary_data) * 8 # Length in bits
    header = f'{data_length:032b}' # 32-bit string header
    header_chunks = [header[i: i + 8] for i in range(0, 32, 8)] # Converts 32-bit string to 8-bit chunks

    binary_data = header_chunks + binary_data # Appends header to the start of the binary data
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
    image.save(image_name)

    print('Success! Image created') # DEBUG
    end_time = time.perf_counter()
    elapsed = end_time - function_start_time
    data_size = len(binary_data) / (1024 ** 2)
    print(f'{data_size:.4f} MB of data converted to images in {elapsed:.4f} s')
    print(f'Data processed at {data_size / elapsed:.4f} MB/s\n')
    return 1 # Done!
    
def compare_data(input_data, output_data):
    """ Compares input_data against output_data for inconsistencies
        Files must be of same type and order 
    """
    print(f'Data testing started. In: {len(input_data)} Bytes     Out: {len(output_data)} Bytes')
    try:
        correct_data = 0
        for i in range(len(output_data)):
            if input_data[i] == output_data[i]:
                correct_data += 1
    except IndexError:
        print('IndexError: Some data must be missing!')
    print(f'Data compared, {correct_data} correct datapoints vs {len(input_data)} datapoints -> {correct_data / len(input_data) * 100}% accurate\n')
    return 1 # Done!

def extract_image_data(imagepath, mode='RGB', outpath='output_data.bin'):
    """ Extracts the binary data from an image and returns it - default mode is RGB, but L can also be used for grey """
    function_start_time = time.perf_counter()
    try:
        # Ensures the mode is valid
        if mode.upper() not in ['RGB', 'L']:
            raise ValueError(f'Unsupported mode "{mode}". Use "L" or "RGB".')
        
        img = Image.open(imagepath) # Opens image
        img = img.convert(mode.upper()) # Uses the specified mode
        
        pixels = list(img.getdata()) # Collects pixel data

        # Converts pixel data to binary
        binary_data = ''
        if mode.upper() == 'L':
            # Greyscale
            
            # Reads header seperately
            header_chunks = pixels[:4]
            header = ''.join(f'{chunk:08b}' for chunk in header_chunks)
            valid_data_length = int(header, 2) # Bytes of data

            # Reads Pixel Data
            for pixel in pixels[4: 4 + valid_data_length // 8]:
                binary_data += f'{pixel:08b}'
        
        elif mode.upper() == 'RGB':
            # RGB 3 Channels

            # Reads header seperately
            header_chunks = [value for pixel in pixels[:2] for value in pixel] # 2 RGB Values -> 6 Bytes (But only 4 used)
            header = ''.join(f'{chunk:08b}' for chunk in header_chunks[:4]) # 4 * 8-bits -> 32-bit header
            valid_data_length = int(header, 2) # Bytes of data (3 * number of pixels)

            # Messy 2 bytes from the remainder of the pixel data used in the header
            remaining_data = header_chunks[4:6]
            binary_data = ''.join(f'{b:08b}' for b in remaining_data)

            # Reads Pixel Data
            num_pixels = (valid_data_length - 16) // 24
            for r, g, b in pixels[2: 2 + num_pixels]:
                binary_data += f'{r:08b}{g:08b}{b:08b}'

        # Writes to file
        with open(outpath, 'wb') as f:
            for i in range(0, len(binary_data), 8):
                byte = int(binary_data[i:i+8], 2)
                f.write(bytes([byte]))
        
    except ValueError as e:
        print(f'ValueError: {e} Unsupported mode. Use "L" or "RGB".')
    except FileNotFoundError:
        print(f'File not found: {imagepath}    Try checking your spelling and file type')
    except Exception as e:
        print(f'An error occured {e}')
    
        
    # DEBUG
    end_time = time.perf_counter()
    print('Success! Image extracted')
    # print(binary_data) # DEBUG
    elapsed = end_time - function_start_time
    data_size = valid_data_length / (1024 ** 2)
    print(f'{data_size:.4f} MB of image data extracted in {elapsed:.4f} s')
    print(f'Data extracted at {data_size / elapsed:.4f} MB/s\n')
    return binary_data


# binary_strings = binary_only_input()
# text_file_to_binary('pi.txt')
# binary_to_text(binary_strings)
# text_to_binary()
# binary_to_grey_image(image_width=1024, image_height=1024, binary_data=text_file_to_binary('pi.txt'))
# binary_to_RGB_image(image_width=2058, image_height=2058, binary_data=text_file_to_binary('Hamilton/shakespeare.txt'))
# extract_image_data('outputRGB.png', 'RGB')

def test_against_pi():
    pi_binary = text_file_to_binary('pi.txt')
    output_pi = binary_to_text(pi_binary)
    with open('pi.txt', 'r') as file:
        real_pi = file.read()   
    compare_data(real_pi, output_pi)

    

def test1(inputfile, outputfile):
    function_start_time = time.perf_counter()
    in_binary = text_file_to_binary(inputfile)
    out_binary = text_file_to_binary(outputfile)
    compare_data(in_binary, out_binary)

    end_time = time.perf_counter()
    elapsed = end_time - function_start_time
    print(f'test1 time taken: {elapsed:.4f} s')

# test1('pi.txt', 'output_data.bin')

def complete_test(input_text, mode='RGB', ouput_name='TEST_output.bin'):
    """ Complete Testing Scenario using input_text filepath 
        Use mode='RGB' for RGB or 'L' for grey 
    """
    print('--  Starting test  --')
    function_start_time = time.perf_counter()

    # TEST
    in_binary = text_file_to_binary(input_text)
    if mode.upper() == 'RGB':
        binary_to_RGB_image(image_width=2048, image_height=4096, binary_data=in_binary, image_name='RGBTEST_output.png')
        extract_image_data('RGBTEST_output.png', 'RGB', ouput_name)
    elif mode.upper() == 'L':
        binary_to_grey_image(image_width=2048, image_height=4096, binary_data=in_binary, image_name='LTEST_output.png')
        extract_image_data('LTEST_output.png', 'L', ouput_name)
    else: 
        print('How do you fuck up a test you buffoon')
    out_binary = text_file_to_binary(ouput_name)
    if not out_binary:
        print(f"Failed to load binary data from {ouput_name}")
        return
    compare_data(in_binary, out_binary)
    # END TEST

    end_time = time.perf_counter()
    elapsed = end_time - function_start_time
    print(f'--  Test time taken: {elapsed:.4f} s  --\n')

# complete_test(input_text='pi.txt', mode='L')
# test_against_pi()
complete_test(input_text='pi.txt', mode='L', ouput_name='LTEST.bin')
complete_test(input_text='pi.txt', mode='RGB', ouput_name='RGBTEST.bin')

# END TIMER
# end_time = time.perf_counter()
# elapsed = end_time - PROGRAM_START_TIME
# print(f'Total program time taken: {elapsed:.4f} s')
