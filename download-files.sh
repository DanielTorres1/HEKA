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


if [ "$nube" = "amazon" ] || [ "$nube" = "digital" ]; then

    echo "Comprimiendo"
    for i in {1..4}; do
        index=$i
        ssh kali-"$nube-"$index "cd /root/HACKING && rm -f ${country}${i}.tar.gz && tar -zcvf ${country}${i}.tar.gz ${country}${i}"
    done

    echo "descargando"
    for i in {1..4}; do
        index=$i
        scp kali-"$nube-"$index:/root/HACKING/${country}${i}.tar.gz .
    done

    echo "descomprimiendo"
    for i in {1..4}; do
        tar -zxvf ${country}${i}.tar.gz 
        rm ${country}${i}.tar.gz 
    done
fi




#todas
if [ "$nube" = "todas" ]; then
    echo "Comprimiendo"
    for i in {1..4}; do
        index=$i
        ssh kali-amazon-$index "cd /root/HACKING && rm -f ${country}${i}.tar.gz && tar -zcvf ${country}${i}.tar.gz ${country}${i}"
    done
    for i in {5..8}; do
        index=$((i-4))
        echo "ssh kali-digital-$index \"cd /root/HACKING && rm -f ${country}${i}.tar.gz && tar -zcvf ${country}${i}.tar.gz ${country}${i}\""
        ssh kali-digital-$index "cd /root/HACKING && rm -f ${country}${i}.tar.gz && tar -zcvf ${country}${i}.tar.gz ${country}${i}"
    done



    echo "descargando"
    for i in {1..4}; do
        index=$i
         scp kali-amazon-$index:/root/HACKING/${country}${i}.tar.gz .
    done
    for i in {5..8}; do
        index=$((i-4))
        scp kali-digital-$index:/root/HACKING/${country}${i}.tar.gz .
    done


    echo "descomprimiendo"
    for i in {1..8}; do
        tar -zxvf ${country}${i}.tar.gz 
        rm ${country}${i}.tar.gz 
    done
fi

echo "Uniendo logs y BDs"

merge-db.py $country

