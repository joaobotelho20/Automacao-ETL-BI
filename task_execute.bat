@echo off
cd "C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI"
echo Iniciando ETL em %DATE% %TIME% >> registro_automacao.txt
"C:\Program Files\Python311\python.exe" ETL-acadweb.py >> registro_automacao.txt 2>&1
echo Finalizado em %DATE% %TIME% >> registro_automacao.txt
echo. >> registro_automacao.txt
