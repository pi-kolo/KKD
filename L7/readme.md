Zestaw programów:
* noise.py - z prawdopodobieństwem p zmienia każdy bit w pliku
    użycie: 
    ```
    python noise.py p in out
        ```
* check.py - zlicza ile razy razy kolejne bloki czterobitowe różnią się w dwu programach
    użycie: 
    ```
    python check.py in1 in2
    ```
* coder.py - koduje plik rozszerzonym kodem Hamminga (8,4)
    użycie: 
    ```
    python coder.py in out
    ```
* decoder.py - dekoduje plik kodem Hamminga (8,4), korygując jeśli wystąpił jeden błąd oraz zliczająć podwójny błąd w danym słowie kodowym
    użycie: 
    ```
    python decoder.py in out
    ```