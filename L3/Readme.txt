Piotr Kołodziejczyk

Program realizuje funkcjonalność kodowania i dekodowania algorytmem LZW, z pośrednim kodowanie Eliasa (gamma, omega i delta) lub Fibonacciego

usage: lzw.py [-h] [-d | -g | -f] [-D | -E] in_file out_file

positional arguments:
  in_file          Input file
  out_file         Output file

optional arguments:
  -h, --help       show this help message and exit
  -d, --delta      Elias delta encoding
  -g, --gamma      Elias gamma encoding
  -f, --fibonacci  Fibonacci encoding
  -D, --decode
  -E, --encode