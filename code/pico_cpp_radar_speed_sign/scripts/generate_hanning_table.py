import math

NUM_STEPS = 1000

sine_table = []
for i in range(NUM_STEPS):
    sine_table.append(round(math.sin(math.pi * i / NUM_STEPS) * 2**15))

hanning_table_str_list = [f"{val}" for val in sine_table]
for i in range(NUM_STEPS):
    if i > 0 and i % 10 == 0:
        hanning_table_str_list[i]+=",\n\t"
    else:
        hanning_table_str_list[i]+= ", "
print("int16_t kHanningTableInt16 = {\n\t" + "".join(hanning_table_str_list) + "\n};")
