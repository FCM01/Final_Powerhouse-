from random import seed
from random import randint
import json

lpt = []
rpt = []
lpt_operations_array = []
rpt_operations_array = []


def encryption_key_refine(encrypt_key):
    true_key_array = []
    temp_value = 0
    temp_storage = []
    for i in encrypt_key:
        temp_storage.append(i)
    i = ord(temp_storage[3]) * 3
    y = ord(temp_storage[7]) * 3
    i_big = True
    y_big = True
    while i_big:
        if i > 50:
            i = i / 20
        if isinstance(i, int) == True:
            temp_value = i
            true_key_array.append(temp_value)
            i_big = False
        elif isinstance(i, int) == False:
            temp_value = int(i + 10)
            true_key_array.append(temp_value)
            i_big = False

    while y_big:

        if y > 50:
            y = y / 20
        if isinstance(y, int) == True:
            temp_value = y
            true_key_array.append(temp_value)
            y_big = False
        elif isinstance(y, int) == False:
            temp_value = int(y + 10)
            true_key_array.append(temp_value)
            y_big = False
    return true_key_array


def reverse_step_two(lpt, rpt, array2, encrypt_key, file_name):

    reverse_array_lpt = []
    reverse_array_rpt = []

    data = array2
    for i in data["lpt_reverse_array"]:
        reverse_array_lpt.append(i)
    for i in data["rpt_reverse_array"]:
        reverse_array_rpt.append(i)
    round_encryption_number1 = encrypt_key[0]
    round_encryption_number2 = encrypt_key[1]
    reversed_array_lpt = []

    cal2_lpt = []
    loop_control = len(lpt)
    for i in range(0, loop_control):
        value1 = lpt[i]
        operation = reverse_array_lpt[i]
        if operation == 1:
            value = value1 - round_encryption_number2
        elif operation == 2:
            value = int(value1 / round_encryption_number2)
        elif operation == 3:
            value = value1 + round_encryption_number2
        cal2_lpt.append(value)
    r_lpt = []
    for i in cal2_lpt:
        # XOR calculation
        value = i ^ round_encryption_number1
        r_lpt.append(value)

    cal2_rpt = []
    loop_control = len(rpt)

    for i in range(0, loop_control):
        value = rpt[i]
        operation = reverse_array_rpt[i]
        if operation == 1:
            value = value - round_encryption_number2
        elif operation == 2:
            value = int(value / round_encryption_number2)
        elif operation == 3:
            value = value + round_encryption_number2
        cal2_rpt.append(int(value))
    r_rpt = []
    for i in cal2_rpt:
        # XOR calculation
        value = i ^ round_encryption_number1
        r_rpt.append(value)
    bytearray1 = []
    for i in r_lpt:
        bytearray1.append(i)
    for i in r_rpt:
        bytearray1.append(i)
    return bytearray1


def reverse_third_step(combined_array, array2, key, file_name):
    lpt = []
    rpt = []
    final_data_array = []
    fixed_key = encryption_key_refine(key)
    # uneven number array
    if len(combined_array) % 2 == 1:
        extra_value = len(combined_array)
        x = len(combined_array)
        max = int(x / 2)
        for i in range(max):
            lpt.append(combined_array[i])
        for i in range(max, len(combined_array)):
            rpt.append(combined_array[i])
        final_data_array = reverse_step_two(lpt, rpt, array2, fixed_key, file_name)
    elif len(combined_array) % 2 == 0:
        max = int(len(combined_array) / 2)
        for i in range(0, max):
            lpt.append(combined_array[i])
        for i in range(max, len(combined_array)):
            rpt.append(combined_array[i])
        final_data_array = reverse_step_two(lpt, rpt, array2, fixed_key, file_name)
    return final_data_array


class Decrptor:
    def powerhouse_reverse(self, array, array2, key, file_name):
        reversed_bytearray = reverse_third_step(array, array2, key, file_name)
        return reversed_bytearray

    