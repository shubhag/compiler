f = open('parselog3.txt','r')
g = open('parselog.dot','w')
g.write('graph parsetree{\n')
i = 0
for line in f:
	if i%2 == 0:
		maggu = line.split('->')
		# part1 = maggu[0]
		# part2 = maggu[1].strip().split(' ')
		# for var in part2:
		# 	g.write('\t')
		# 	g.write(part1)
		# 	g.write('-- ')
		# 	if len(var) == 1:
		# 		g.write('"')
		# 		g.write(var)
		# 		g.write('"')
		# 		g.write(';\n')
		# 	else:
		# 		g.write(var)
		# 		g.write(';\n')
		i += 1
	else:
		i += 1
g.write('}\n')
f.close()
g.close()	