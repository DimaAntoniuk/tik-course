def main ():
    number = 533
    h_code = hamming_code(number)
    decoded_number = decode_from_hamming_code(h_code)
    print(f'Hamming code of input number({number}): {h_code}')
    print(f'Decodeding result: {decoded_number}')

    print('\n\nTest:\n')
    test_h_code = dec_to_bin(int(h_code, 2) ^ 1 << 4)
    print(f'Hamming code with mistake: {test_h_code}')
    test_decoded_number = decode_from_hamming_code(test_h_code)
    print(f'Decoded number: {test_decoded_number}\n')
    print('Checking...\n')
    if decoded_number == test_decoded_number :
        print('Result: Done')
    else :
        print('Result: Error')

def dec_to_bin(number):
    return bin(number)[2:] 

def count_bin_number(number):
    return len(number.replace('0', ''))



def hamming_code(number):
    bin_code = dec_to_bin(number)
    m = len(bin_code)
    redundant_bits = calcRedundantBits(m)
    h_code = posRedundantBits(bin_code, redundant_bits)
    h_code = calcParityBits(h_code, redundant_bits)
    return h_code

def decode_from_hamming_code(h_code):
    r = calcRedundantBits(len(h_code), full_code=True)
    pos_r_bits = [2**i - 1 for i in range(r)]
    h_code = h_code[::-1]
    r_bits = ''
    number = ''
    for i in range(len(h_code)):
        if i in pos_r_bits:
            r_bits += h_code[i]
        else :
            number += h_code[i]

    h_code_decoded_number = hamming_code(int(number[::-1], 2))[::-1]
    if h_code_decoded_number != h_code:
        r_bits_decoded_number = ''
        for i in range(r):
            r_bits_decoded_number += h_code_decoded_number[pos_r_bits[i]]
        wrong_bit = 0
        for i, j, k in zip(range(r), r_bits, r_bits_decoded_number):
            if j != k:
                wrong_bit += 2 ** i
        if h_code[wrong_bit - 1] == '0':
            h_code = h_code[:wrong_bit - 1] + '1' + h_code[wrong_bit:]
        else:
            h_code = h_code[:wrong_bit - 1] + '0' + h_code[wrong_bit:]
        number = decode_from_hamming_code(h_code[::-1])
    
    if isinstance(number, int):
        return number
    return int(number[::-1], 2)



def calcRedundantBits(m, full_code = False): 
    '''
        Use the formula 2 ^ r >= m + r + 1 
        to calculate the no of redundant bits.  
    '''
    if not full_code:
        for i in range(m): 
            if 2 ** i >= m + i + 1: 
                return i
    else :
        for i in range(m):
            if 2 ** i >= m + 1:
                return i
  
  
def posRedundantBits(data, r): 
    '''
        Redundancy bits are placed at the positions 
        which correspond to the power of 2. 
    '''
    j = 0
    k = 1
    m = len(data) 
    res = '' 
   
    for i in range(1, m + r+1): 
        if(i == 2**j): 
            res = res + '0'
            j += 1
        else: 
            res = res + data[-1 * k] 
            k += 1
   
    return res[::-1] 
  
  
def calcParityBits(arr, r): 
    n = len(arr) 
    for i in range(r): 
        val = 0
        for j in range(1, n + 1): 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(arr[-1 * j]) 
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:] 
    return arr 
  
  
def detectError(arr, r): 
    n = len(arr) 
    res = 0
    for i in range(r): 
        val = 0
        for j in range(1, n + 1): 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(arr[-1 * j]) 
  
        res = res + val*(10**i) 
    return int(str(res), 2)

if __name__ == '__main__':
   main() 