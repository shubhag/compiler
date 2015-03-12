grep "Reduce" < parselog.txt | grep -o '\[.*\]' | tac | sed -e 's/ with /\n/g' | sed 's/^.//' | awk '{print substr($0, 0, length($0))}' > parselog3.txt 
python script.py 
dot -Tps parse_tree.dot -o out.ps