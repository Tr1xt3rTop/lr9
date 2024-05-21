import collections
import numpy as np
from addit_functs import mod_on_2, reverse_bit, read_color, text_to_binary, subarr_extract, \
    number_to_bin_arr, bin_arr_to_number, binary_to_text, save_color

# Define the Hamming matrix for error detection and correction
H = np.matrix([
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
], dtype=int)
n = 15  # Length of the codeword

def encode(codeword_bits, message_bits):
    codeword = np.matrix(codeword_bits, dtype=int)
    message = np.matrix(message_bits, dtype=int)
    syndrome = mod_on_2(H * codeword.T) + message.T
    syndrome = mod_on_2(syndrome).T.tolist()[0]
    error_position = (8 * syndrome[3] + 4 * syndrome[2] + 2 * syndrome[1] + syndrome[0]) - 1

    if error_position >= 0:
        codeword_bits = reverse_bit(codeword_bits, error_position)

    return codeword_bits

def decode(codeword_bits):
    message_bits = mod_on_2(H * np.matrix(codeword_bits, dtype=int).T)
    return message_bits.T.tolist()[0]

def embed_text(image, text, start_marker, end_marker, offset):
    binary_text = text_to_binary(start_marker) + text_to_binary(text) + text_to_binary(end_marker)
    lsb_array = [number_to_bin_arr(byte)[-1] for byte in image]

    start_index = offset * n
    for byte in binary_text:
        message_bits = number_to_bin_arr(byte)[:4]
        for i in range(0, len(message_bits), 4):
            codeword_bits = lsb_array[start_index:start_index + n]
            codeword_bits = encode(codeword_bits, message_bits)
            lsb_array[start_index:start_index + n] = codeword_bits
            start_index += n

    new_image = update_image_from_lsb(image, lsb_array)
    return new_image

def extract_text(image, start_marker, end_marker):
    lsb_array = [number_to_bin_arr(byte)[-1] for byte in image]
    message_bits = []

    for i in range(0, len(lsb_array), n):
        if len(lsb_array[i:i + n]) < n:
            break
        message_bits.extend(decode(lsb_array[i:i + n]))

    text_bits = subarr_extract(text_to_binary(start_marker), message_bits, text_to_binary(end_marker))
    text_bytes = [bin_arr_to_number(text_bits[i:i + 8]) for i in range(0, len(text_bits), 8)]
    return binary_to_text(text_bytes)

def update_image_from_lsb(image, lsb_array):
    new_image = []
    for i, byte in enumerate(image):
        bit_array = number_to_bin_arr(byte)
        bit_array[7] = lsb_array[i]
        new_image.append(bin_arr_to_number(bit_array))
    return new_image

if __name__ == '__main__':
    path_to_image = "flag.jpg"
    image_pixels = read_color(path_to_image, 'pixels')
    secret_text = "Hello world! Как дела? Привет мир!!!"
    marker_start = "#d*&63ls"
    marker_end = "&2KJH349"

    encoded_image = embed_text(image_pixels, secret_text, marker_start, marker_end, 15)
    decoded_text = extract_text(encoded_image, marker_start, marker_end)
    save_color(path_to_image, encoded_image, 'pixels')

