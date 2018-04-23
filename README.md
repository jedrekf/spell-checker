# spell-checker


### Uruchomienie lokalnie mikroserwisu spolszczania

Otworzyć terminal w głównym folderze projektu:
```shell
cd ./microservice/public && php -S localhost:8080
```

Odwiedź http://localhost:8080 

### Korzystanie z mikroserwisu dodającego polskie znaki
Mikroserwis obudowywuje w REST API, SOAP api wystawione przez portal http://www.spolszcz.pl/

Jak skorzystać:
```python
#-*- coding: utf-8 -*-
from preprocess import polish

#output: "Zdanie bez polskich znaków."
print(preprocess.polish("Zdanie bez polskich znakow."))
```

W przypadku używania innego portu niż localhost:8080 go podać w [pliku konfiguracyjnym](config.py) 





