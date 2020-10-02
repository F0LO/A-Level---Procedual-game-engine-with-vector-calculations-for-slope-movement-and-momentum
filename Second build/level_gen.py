import random
#RLE Encoding
def rle_encode(data):
    encoding = ''
    prev_char = ''
    count = 1
    for char in data:
        if char != prev_char:
            if prev_char:
                encoding += str(count) + prev_char
            count = 1
            prev_char = char
        else:
            count += 1
    else:
        encoding += str(count) + prev_char
        return encoding
#Level Gen
list_pos = 0
Generation = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
for i in Generation:
    Ran_num = random.random()
    if Ran_num < 0.7:
        pass
    else:
        Ran_num = random.random()
        if Ran_num < 0.6:
            Generation[list_pos] = "t"
        else:
            Ran_num = random.randint(1,6)
            Generation[list_pos] = str(Ran_num)
    list_pos += 1
Gen_string = "".join(Generation)
print("Raw String: '",Gen_string,"'")
print("RLE String:", rle_encode(Gen_string))
