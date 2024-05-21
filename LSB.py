from addit_functs import *
import random

TB_old = []
TB_new = []


def LSB_R_enc(img, text, start, end, sdvig, raid=0.25):
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    raid = round(3 / raid)
    index = round(sdvig * raid)

    array_LSB = []
    for ch in binary_text:
        arr_bit_ch = number_to_bin_arr(ch)
        for bit in arr_bit_ch:
            if bit == 0:
                img[index] = clear_bit(img[index], 0)
            else:
                img[index] = set_bit(img[index], 0)
            bits = number_to_bin_arr(img[index])
            array_LSB.append(bits[7])
            index += raid

    for i in range(0, len(array_LSB), 8):
        byte = bin_arr_to_number(array_LSB[i:i + 8])
        TB_old.append(byte)

    return img


def LSB_M_enc(img, text, start, end, sdvig, raid=0.25):
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    raid = round(3 / raid)

    index = round(sdvig * raid)
    for ch in binary_text:
        arr_bit_ch = number_to_bin_arr(ch)
        for bit in arr_bit_ch:
            bit_img = retn_bit(img[index], 7)
            if bit == 0 and bit_img == 0:
                index += raid
                continue
            elif bit == 0 and bit_img == 1:
                if img[index] == 255:
                    img[index] = img[index] - 1
                else:
                    rand_bit = random.randrange(-1, 2, 2)
                    img[index] = img[index] + rand_bit
            elif bit == 1 and bit_img == 0:
                if img[index] == 0:
                    img[index] = img[index] + 1
                else:
                    rand_bit = random.randrange(-1, 2, 2)
                    img[index] = img[index] + rand_bit
            elif bit == 1 and bit_img == 1:
                index += raid
                continue

            index += raid

    return img


def LSB_dec(img, start, end, raid=0.25):
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
        TB_new.append(byte)



    return binary_to_text(text_byte)


def main():
    path_to_image = "flag.jpg"
    image = read_color(path_to_image, 'pixels')
    text = "Hello world! Как дела? Привет мир!!!"
    m_start = "1"
    m_end = "2"

    text = "HW"

    image = LSB_R_enc(image, text, m_start, m_end, 5, 0.25)
    orig_text = LSB_dec(image, m_start, m_end, 0.25)



    # save_color(path_to_image, image, 'pixels')

    print(orig_text)


if __name__ == '__main__':
    main()
