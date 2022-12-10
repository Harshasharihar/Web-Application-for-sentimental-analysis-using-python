# encryption
from datetime import date
import random

usr_names = ['srirang', 'abdal', 'mallu', 'harsha']
selected = random.choice(usr_names)
# print(selected)
number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
num_select = random.choice(number)
for ind, al in enumerate(number):
    if num_select == al:
        nindex = ind
# print(num_select)
today = str(date.today())
encrypt = []
# print("Today date is: ", today)
day = today[-2:]
final_usr = selected + day
# print(final_usr)
encrypt = list(selected)
# print(encrypt)
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
new_encrypt = []

ele, koo = 0, 0
for n in encrypt:
    for ele in range(0, len(alpha)):
        if n == alpha[ele]:
            sell = alpha[ele + num_select]
            new_encrypt.append(sell)
encryption = ''.join(new_encrypt)
# print(encryption)
symbols = [')','!','@','#','$','%','^','&','*','(']
num_day = []
for k in day:
    if k == '0':
        num_day.append(symbols[0])
        # num_day.append("'")
    else:
        num_day.append(symbols[int(k)])
        # num_day.append("'")
n_day = "".join(num_day)
fin_symbol = symbols[nindex]
password = encryption + n_day+ fin_symbol
print(password)

# decryption
en = []
dec = list(password)
# print(dec)
for q, loo in enumerate(symbols):
    if loo == dec[-3]:
        day1 = loo
        en.append(str(q))
for qo, loof in enumerate(symbols):
    if loof == dec[-2]:
        day2 = loof
        en.append(str(qo))
for qoo, loofw in enumerate(symbols):
    if loofw == dec[-1]:
        select_num = qoo
        en.append(str(qoo))
decen = "".join(en)
# print(decen)
new_decrypt = []
for m in dec[0:-3]:
    for ele in range(0, len(alpha)):
        if m == alpha[ele]:
            cell = alpha[ele - select_num]
            new_decrypt.append(cell)
decryption = ''.join(new_decrypt)
# print(decryption)
decrypted_pwd = decryption + decen
print(decrypted_pwd)