tree_file = open("parse_tree.dot", "w")

tree_file.write("digraph \"Parse Tree\" {\n")

i = 1
j = 0 
node_terminals = {}
with open("parselog3.txt", "r") as f:
	for line in f.readlines():
		if (i%2) == 1:
			prod_lhs = line.split(" -> ")[0]
			prod_rhs = line.split(" -> ")[1]
			if j != 0 :
				value = node_terminals.get(prod_lhs, 0)
				prod_lhs = prod_lhs + str(value)
			j = j + 1 
			rhs_tokens = prod_rhs.split()

			rhs_string = "{ ";
			for token in rhs_tokens :
				if len(token) == 1 :
					token = "\"" + token + "\""
					rhs_string = rhs_string + " " + token;
				else :
					value = node_terminals.get(token, 0)
					node_terminals[token] = value + 1 ;
					tree_file.write("\t"+token+str(node_terminals[token])+" [label = \"" +token+ "\"] \n")
					rhs_string = rhs_string + " " + token + str(node_terminals[token]);
			# print ' '.join(rhs_tokens)
			rhs_string = rhs_string + " }"
			tree_file.write("\t" + prod_lhs + " -> " + rhs_string + "\n")
		i = i + 1
		
tree_file.write("\n}")

tree_file.close()

