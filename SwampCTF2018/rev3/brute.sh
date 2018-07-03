
while true
do
	if [ `./OS.BIN_patched | tee -a running | grep "GRANTED"  | wc -l` -ge 1 ]
	then
		echo "GRANTED"
		sleep 6
		echo "TRY"
		nc chal1.swampctf.com 1313 &
		sleep 3
		echo "TRY"
		nc chal1.swampctf.com 1313 &
	fi
	sleep 0.5
done
