#!/bin/bash

# Default values
country='Peru'
nube='digital'

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --country)
        country="$2"
        shift
        shift
        ;;
        --nube)
        nube="$2"
        shift
        shift
        ;;
        *)
        # unknown option
        shift
        ;;
    esac
done

# Nombre del archivo de entrada
archivo="SUBNETS-${country}2.txt"


# Calcula el número de líneas por archivo, dejando 3 líneas para el último archivo

if [ "$nube" = "todas" ]; then
    # Cuenta el número total de líneas en el archivo
    total_lineas=$(( $(wc -l < "$archivo") + 7 ))
    lineas_por_archivo=$(( (total_lineas ) / 8 ))
else
    # Cuenta el número total de líneas en el archivo
    total_lineas=$(( $(wc -l < "$archivo") + 3 ))
    lineas_por_archivo=$(( (total_lineas ) / 4 ))
fi


# Usa split para dividir el archivo en partes iguales, con las líneas calculadas
split -l $lineas_por_archivo "$archivo" temp_parte_

# Renombra los archivos generados a red_N.txt
contador=1
for f in temp_parte_*
do
    mv "$f" "red_${contador}.txt"
    contador=$((contador + 1))
done

if [ "$nube" = "amazon" ]; then
    # Subir archivos a la nube correspondiente
    for i in {1..4}; do
        echo "Subiendo red_${i}.txt"
        ssh kali-amazon-$i 'rm /root/HACKING/red* /root/HACKING/archivo.log'
        scp red_${i}.txt kali-amazon-$i:/home/admin && ssh kali-amazon-$i "sudo mv /home/admin/red_${i}.txt /root/HACKING"    
    done
fi

if [ "$nube" = "digital" ]; then
    for i in {1..4}; do
        ssh kali-digital-$i 'rm /root/HACKING/red* /root/HACKING/archivo.log'
        scp red_${i}.txt kali-digital-$i:/root/HACKING
    done
fi

if [ "$nube" = "todas" ]; then
    for i in {1..4}; do
        echo "Subiendo red_${i}.txt"
        ssh kali-amazon-$i 'rm /root/HACKING/red* /root/HACKING/archivo.log'
        scp red_${i}.txt kali-amazon-$i:/home/admin && ssh kali-amazon-$i "sudo mv /home/admin/red_${i}.txt /root/HACKING"    
    done

    for i in {5..8}; do
        index=$((i-4))
        ssh kali-digital-$index 'rm /root/HACKING/red* /root/HACKING/archivo.log'
        scp red_${i}.txt kali-digital-$index:/root/HACKING
    done
fi