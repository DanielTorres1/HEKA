#!/bin/bash
# Default values
country='bolivia'
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

echo "Comprimiendo"
for i in {1..4}; do
    ssh kali-"$nube-"$i "cd /home/kali/HACKING && rm -f ${country}${i}.tar.gz && tar -zcvf ${country}${i}.tar.gz ${country}${i}"
done

echo "descargando"
for i in {1..4}; do
    scp kali-"$nube-"$i:/home/kali/HACKING/${country}${i}.tar.gz .
done

echo "descomprimiendo"
for i in {1..4}; do
    tar -zxvf ${country}${i}.tar.gz 
    rm ${country}${i}.tar.gz 
done

echo "Uniendo logs y BDs"

python merge-db.py $country

