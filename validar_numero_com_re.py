import re

phone_number = input("")  

def validate_numero_telefone(phone_number):
   
 
    if re.match(pattern, phone_number):  
        return "Número de telefone válido"
        
    else:
        return "Número de telefone inválido"

pattern = r"^\([1-9]{2}\) (?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$"



result = validate_numero_telefone(phone_number)

print(result)