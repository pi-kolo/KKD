Program coders.py koduje i dekoduje obrazy *.tga. Kodowanie obrazu zwraca dwa zakodowane pliki, drugi z nałożonym filtrem dolnoprzepustowym 
i zakodowany różnicowo i pierwszy z filtrem górnoprzepustowym zakodowany z k-bitowym kwantyzatorem nierównomiernym.

Użycie:
* kodowanie: 
  ```python coders.py -e k plik_in plik_out_H plik_out_L```
* dekodowanie: ```python coders.py -d k -H/-L plik_in plik_out```