grep "Reduce" < parselog.txt 
grep -o '\[[^\[]*\]' parselog2.txt > parselog3.txt

grep "Reduce" < parselog.txt | grep -o '\[[^\[]*\]' > parselog3.txt
