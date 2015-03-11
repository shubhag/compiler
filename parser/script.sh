grep "Reduce" < parselog.txt 
grep -o '\[[^\[]*\]' parselog2.txt > parselog3.txt

grep "Reduce" < parselog.txt | grep -o '\[[^\[]*\]' > parselog3.txt

grep "Reduce" < parselog.txt | grep -o '\[.*\]' | tac | sed -e 's/with /\n/g' | sed 's/^.//' | awk '{print substr($0, 0, length($0))}' > parselog3.txt 


grep "Reduce" < parselog.txt | grep -o '\[.*\]' | tac | sed -e 's/ with /\n/g' | sed 's/^.//' | awk '{print substr($0, 0, length($0))}' > parselog3.txt 