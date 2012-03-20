import re
#a = '((a=b)&&((b=C)||(y=z)))&&((d=e)&&(f=g))'
#b = '((a=b)&&((b=C)||(y=z)))||((d=e)&&(f=g))'

#This function returns the left operand, the operator and the right operand of a complex condition

def Split_Complex_Condition(string):
        
        clean = re.compile(r'[\s]*(not)?[\s]*\((.+)\)') #get the structure of the left and right operands
        salida = ''
        leftOP = ''
        operator = ''
        rigthOP = ''
        parent = 0
        char = 0
        
        for i in string:
                salida += i
                char += 1
                if i == '(':                            
                        parent += 1
        
                elif i == ')': 
                        parent -= 1

                if (parent == 0) and ((i == '|')or (i == '&')):

                        #if clean.search(salida).group(1) == None:
                        leftOP = clean.search(salida).group(2)
                        #else:
                        #        leftOP = "not" + clean.search(salida).group(2)

                        #if clean.search( string[char:len(string)]).group(1) == None:
                        rightOP = clean.search( string[char:len(string)]).group(2)
                        #else:
                        #        rightOP ="not" +  clean.search( string[char:len(string)]).group(2)

			operator = i + i
                        return leftOP, rightOP, operator
                                
                else:   
                        salida += ''



