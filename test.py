import re
word = str("S AH1 M {onset: S, nucleus: AH1, coda: M} T AY2 M {onset: T, nucleus: AY2, coda: M}")
print(word)
#temp = re.sub(r'\{.*?\}','', word)
#print(temp)




#separate to get the onset, nucleus and coda from each word
temp = re.sub(r'\{.*?\}','', str(word))
print(temp)
                    
#splits into parts and removes the numbers from the onset, nucleus and coda
parts = (re.sub(r'\d+', '',temp)).split(" ")  #using google search: https://www.geeksforgeeks.org/python/python-ways-to-remove-numeric-digits-from-given-string/
print(parts)
for part in parts:
    if part == "":
        parts.remove(part)
print(parts)
# {.*?} .=wildcard, *=any number of, ?=optionally the thing before   === is this is is there a bracket and stuff inside and it removes it