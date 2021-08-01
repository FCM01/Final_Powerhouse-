from random import seed
from random import randint
import json
lpt = []
rpt = []
lpt_operations_arrary = []
rpt_operations_arrary = []


def encryption_key_refine(encrypt_key):
    try:
        true_key_array = []
        temp_value  = 0
        temp_storage =[]
        for i in encrypt_key:
            temp_storage.append(i)
        i = ord(temp_storage[3])*3
        y = ord(temp_storage[7])*3

        i_big = True
        y_big = True

        while(  i_big ):
            if i > 50:
                i= i/20
            if isinstance(i, int)==True:
                temp_value = i
                true_key_array.append(temp_value)
                i_big  = False
            elif isinstance(i, int)==False:
                temp_value = int(i + 10)
                true_key_array.append(temp_value) 
                i_big  = False

        while(y_big ):
            
            if y > 50:
                y= y/20
            if isinstance(y, int)==True:
                temp_value = y
                true_key_array.append(temp_value)
                y_big  = False
            elif isinstance(y, int)==False:
                temp_value = int(y + 10)
                true_key_array.append(temp_value) 
                y_big  = False
                
        return true_key_array
    except Exception as e  :
        print("ERROR-in->encryption_key_refine>>>:", e)
    

def reverse_step_two(lpt,rpt,data,encrypt_key,file_name):
    try:
        print("Decrypting.......")
        reverse_array_lpt = []
        reverse_array_rpt = []
        for i in data["lpt_reverse_array"]:
            reverse_array_lpt.append(i)
        for i in data["rpt_reverse_array"]:
            reverse_array_rpt.append(i)
        round_encryption_number1 = encrypt_key[0]
        round_encryption_number2 = encrypt_key[1]
        reversed_array_lpt= []

        cal2_lpt = []
        loop_control  = len(lpt)
        
        for i in range(0,loop_control):
            value1 = lpt[i]        
            operation  =  reverse_array_lpt[i]
            if operation == 1 :
                value =  value1 - round_encryption_number2
            elif operation  == 2:
                value =   int(value1 / round_encryption_number2)
            elif operation == 3:
                value =  value1 + round_encryption_number2
            cal2_lpt.append(value)
        
        r_lpt = []
        for i in cal2_lpt:
                # XOR calculation
                value = i ^ round_encryption_number1
                r_lpt.append(value)
        cal2_rpt = []
        loop_control  = len(rpt)

        for i in range(0,loop_control):
            value = rpt[i]        
            operation  = reverse_array_rpt[i]
            if operation == 1 :
                value =  value - round_encryption_number2
            elif operation  == 2:
                value =  int(value / round_encryption_number2)
            elif operation == 3:
                value =  value + round_encryption_number2
            cal2_rpt.append(int(value))
        r_rpt = []
        for i in cal2_rpt:
                # XOR calculation
                value = i ^ round_encryption_number1
                r_rpt.append(value)
        #merge of the arrays  to a comabined final array
        bytearray1 =[]
        for i in r_lpt:
            bytearray1.append(i)
        for i in r_rpt:
            bytearray1.append(i)
        print("Returning the array from Powerhouse Heavy Decrypt_Core")
        return bytearray1
    except Exception as e  :
        print("ERROR-in->reverse_step_two>>>:", e)


def reverse_third_step(combined_array,reverse_array,key,file_name):
    try:
        lpt = []
        rpt = []
        print("Now in Powerhouse Heavy Decrypt_Core")
        final_data_array =[]
        fixed_key  = encryption_key_refine(key)
    # uneven number array
        if len(combined_array)% 2 == 1:
            print("Uneven")
            extra_value = len(combined_array)
            x = len(combined_array)
            max = int(x/2)
            for i in range(max):
                lpt.append(combined_array[i])
            for i in range (max,len(combined_array)):
                rpt.append (combined_array[i])
            print("reverse_third_step lpt-->",lpt)
            print("reverse_third_step rpt-->",rpt)
            final_data_array = reverse_step_two(lpt,rpt,reverse_array,fixed_key,file_name)
        elif len(combined_array)% 2 == 0:
            print("Even") 
            max = int(len(combined_array)/2)
            for i in range (max):
                lpt.append(combined_array[i])
            for i in range (max,len(combined_array)):
                rpt.append(combined_array[i])
            print("reverse_third_step lpt>>>:",lpt)
            print("reverse_third_step rpt>>>:",rpt)
            final_data_array = reverse_step_two(lpt,rpt,reverse_array,fixed_key,file_name)
        return final_data_array
    except Exception as e:
        print("ERROR-in->reverse_step_two>>>:", e)
        
        

class Decrptor :

    def powerhouse_decrypt(self,array,reverse_arrays,key,file_name):
        reversed_bytearray = reverse_third_step(array,reverse_arrays,key,file_name)
        return (reversed_bytearray)
   
   