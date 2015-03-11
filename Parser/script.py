import sys

# filename = sys.argv[1]
# f = open(filename)
# data = f.read()
# f.close()

# phrase = "Reduce"
# for line in data:
# 	print line
# 	if "Reduce" in line:
# 		print 'a'
# 		print line

f = open('parselog.txt')
for line in f:
	# print line
	if "Reduce" in line:
		print line
f.close()