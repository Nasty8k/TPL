## Compiler for simple python version
[GCC 9.3.0]
x86_64-linux-gnu

#### Команда для запуска:
```
python3 python3 ./main.py <исходная_программа.py>
```    

Промежуточный файл компиляции находится в директории ./asm/

В результате работы компилятора формируется исполняемый файл в директории ./exe/ 

#### Команда для запуска с опциями:
```
python3 python3 ./main.py [опция] <исходная_программа.py>
```  

##### Опции
    --dump-tokens — вывод работы лексического анализатора
    --dump-ast    — вывод AST
    --dump-asm    — вывод файла ассемблера
