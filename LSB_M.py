from addit_functs import *
from LSB import LSB_R_dec
import random


def LSB_M_enc(img, text, start, end, sdvig, raid=0.25):
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    raid = round(3 / raid)

    bit_img_arr = []
    bit_text = []
    otladka = []
    index = sdvig
    for ch in binary_text:
        arr_bit_ch = number_to_bin_arr(ch)
        for bit in arr_bit_ch:
            bit_text.append(bit)
            bit_img = retn_bit(img[index], 7)
            bit_img_arr.append(bit_img)
            if bit == 0 and bit_img == 0:
                otladka.append(1)
                index += raid
                continue
            elif bit == 0 and bit_img == 1:
                if img[index] == 255:
                    otladka.append(2)
                    img[index] = img[index] - 1
                else:
                    otladka.append(3)
                    rand_bit = random.randrange(-1, 2, 2)
                    img[index] = img[index] + rand_bit
            elif bit == 1 and bit_img == 0:
                if img[index] == 0:
                    otladka.append(4)
                    img[index] = img[index] + 1
                else:
                    otladka.append(5)
                    rand_bit = random.randrange(-1, 2, 2)
                    img[index] = img[index] + rand_bit
            elif bit == 1 and bit_img == 1:
                otladka.append(6)
                index += raid
                continue

            index += raid


    return img


def LSB_M_dec(img, start, end, raid=0.25):
    raid = round(3 / raid)

    array_LSB = []
    for i in range(0, len(img), raid):
        byte = img[i]
        bits = number_to_bin_arr(byte)
        array_LSB.append(bits[7])


    bit_start = []
    for e in text_to_binary(start):
        bit_start = bit_start + number_to_bin_arr(e)

    bit_end = []
    for e in text_to_binary(end):
        bit_end = bit_end + number_to_bin_arr(e)

    text_bit = subarr_extract(bit_start, array_LSB, bit_end)

    text_byte = []
    for i in range(0, len(text_bit), 8):
        byte = bin_arr_to_number(text_bit[i:i + 8])
        text_byte.append(byte)

    return binary_to_text(text_byte)


def main():
    path_to_image = "flag.jpg"
    image = read_color(path_to_image, 'pixels')
    text = "Hello world! Как дела? Привет мир!!!"
    m_start = "#d*&63ls"
    m_end = "&2KJH349"


    image = LSB_M_enc(image, text, m_start, m_end, 0, 3)
    orig_text = LSB_R_dec(image, m_start, m_end, 3)




if __name__ == '__main__':

    main()
