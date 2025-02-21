for i in {01..31};
do
    sar -f /var/log/sysstat/sa$i -r > ./data/$i.txt;
done

last | grep "system boot" > ./data/reboots.txt