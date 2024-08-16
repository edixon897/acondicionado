file_path = r'\\192.168.0.114\D\compartidos\plsaldo.prn'

with open(file_path) as archivo:
    for linea in archivo:
        print(linea.strip())

