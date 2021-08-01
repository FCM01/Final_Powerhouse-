from random import seed
from random import randint
import json



def encryption_key_refine(encrypt_key):
    true_key_array = []
    temp_value  = 0
    temp_storage =[]
    for i in encrypt_key:
        temp_storage.append(i)
    i = ord(temp_storage[3])*3
    y = ord(temp_storage[7])*3
    i_big = True
    y_big = True
    z_big = True

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


def third_step(lpt, rpt ):
    try:
        textdata_array = []
        for i in lpt:
            textdata_array.append(i)
        for j in rpt:
            textdata_array.append(j)
        return textdata_array
        
    except Exception as e:
        print("ERROR-in->third_step>>>:", e)
    
    
def step_two(lpt , rpt, encrypt_key,file_name):
    try:
        # special_character_array = [+,*,-]
        reverse_encryption_key_lpt = []
        reverse_encryption_key_rpt = []

        #lpt shift character  section
        round_encryption_number1 = encrypt_key[0]
        round_encryption_number2 = encrypt_key[1]
        # section operator selection for the reverse array key for lpt 
        round_control_number_lpt  = 0 

        cal1lpt = []
        cal2lpt = []
        #round one
        round_control_number_lpt += 1
        for i in lpt:
            # XOR calculation
            value = 0
            value = i ^ round_encryption_number1
            cal1lpt.append(value)

        #round two
        round_control_number_lpt += 1
        for i in cal1lpt:
            true_operation = randint(1,2)
            reverse_encryption_key_lpt.append(true_operation) 
            # the access of the array lpt values must occur here so that they can be used
            value = 0
            if true_operation == 1 :
                value = i + round_encryption_number2
            elif true_operation  == 2:
                value= i * round_encryption_number2
            elif true_operation == 3:
                value = i - round_encryption_number2
            cal2lpt.append(value)  

        rpt_operations_arrary = []
        round_control_number_rpt  = 0 
        cal1rpt = []
        cal2rpt = []
        #round one
        round_control_number_rpt += 1
        for i in rpt:
            # XOR calculation
            value = 0
            value = i ^ round_encryption_number1
            cal1rpt.append(value)

        #round two
        round_control_number_lpt += 1
        for i in cal1rpt:
            true_operation = randint(1,2)
            reverse_encryption_key_rpt.append(true_operation) 
            # the access of the array lpt values must occur here so that they can be used
            value = 0
            if true_operation == 1 :
                value = i + round_encryption_number2
            elif true_operation  == 2:
                value= i * round_encryption_number2
            elif true_operation == 3:
                value = i - round_encryption_number2
            cal2rpt.append(value)  

        reverse_arrays  = {}
        reverse_arrays = {
            "lpt_reverse_array":reverse_encryption_key_lpt,
            "rpt_reverse_array":reverse_encryption_key_rpt
        }
        
        final_text_data = third_step(cal2lpt,cal2rpt)
        print("Round LPT: ",round_control_number_lpt," :")
        print("Round RPT: ",round_control_number_rpt," :")

        return (reverse_arrays, final_text_data)
    except Exception as e :
        print("ERROR-in->step_two>>>:", e)

class Encrptor:   
   

  # the first step function separatres the byarray in to almost equal arrays 
    def powerhouse(self,bytearray1,key,file_name):
        try:
            lpt = []
            rpt = []
            final_data_array =[]
            fixed_key  = encryption_key_refine(key)
        # uneven number array
            if len(bytearray1)% 2 == 1:
                extra_value = len(bytearray1)
                x = len(bytearray1)
                max = int(x/2)
                for i in range(max):
                    lpt.append(bytearray1[i])
                for i in range (max,len(bytearray1)):
                    rpt.append (bytearray1[i])
                final_data_array = step_two(lpt,rpt,fixed_key,file_name)
            elif len(bytearray1)% 2 == 0:
                max = int(len(bytearray1)/2)
                for i in range (0,max):
                    lpt.append(bytearray1[i])
                for i in range (max,len(bytearray1)):
                    rpt.append(bytearray1[i])
                final_data_array = step_two(lpt,rpt,fixed_key,file_name)  
            return (final_data_array)
        except Exception as  e:
            print("ERROR-in->Powerhouse Class>>>:", e)
            