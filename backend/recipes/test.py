s = {}

try:
    s['123'] += {'amount':10, 'measur':"шт"}
    
except:
    s['123'] = {'amount':10, 'measur':"шт"}
try:
    s['222'] += {'amount':20, 'measur':"л"}
except:
    s['222'] = {'amount':20, 'measur':"л"}

try:
    s['123'] += {'amount':15, 'measur':"шт"}
except:
    s['123'] = {'amount':150, 'measur':"шт"}
s['123']['amount'] += 200
s['222']['amount'] += 500
#print(s)

with open("test.txt", "w", encoding='utf-8') as file:
    for key in s:
        file.write(f'{key} - {s[key]["amount"]} {s[key]["measur"]}\n')

#with open("test.txt", "w", encoding='utf-8') as file:
#    for key in s:        
#        file.write(f'{key} - {s[key]}\n')
#if name not in ingredients_dict:
#                ingredients_dict[name] = {
#                    'measurement_unit': measurement_unit,
#                    'amount': amount
#                    }
#            else:
#                ingredients_dict[name]['amount'] += amount
