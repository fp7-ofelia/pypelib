def Get_Items(List):
	
	string = ""
	i = 0
	for items in List:

		if i == len(List) -1:
			string += str(items) 
		else:
			string += str(items) + ','
			i += 1

	return string.encode('utf-8')
	
		
