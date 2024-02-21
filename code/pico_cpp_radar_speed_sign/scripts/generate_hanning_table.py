import math

kNumHanningSteps = 1000

sine_table = []
for i in range(kNumHanningSteps):
    sine_table.append(round(0.5 * (1 - math.cos(2 * math.pi * i / kNumHanningSteps)) * 2**15))

hanning_table_str_list = [f"{val}" for val in sine_table]
for i in range(kNumHanningSteps):
    if i > 0 and i % 10 == 0:
        hanning_table_str_list[i]+=",\n\t"
    else:
        hanning_table_str_list[i]+= ", "
print("uint16_t kHanningTableUint16[kNumHanningSteps] = {\n\t" + "".join(hanning_table_str_list) + "\n};")
