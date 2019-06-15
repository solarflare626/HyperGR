import os
import sys

table = []
isHGR = True
fails = 0
isError = False
dimension = 0
def main():
    '''
        open file and transform data to table
    '''
    global isError
    global table
    global dimension
    file = open('data.txt','r')
    for line in file:
        # remove '\n' at the end of line
        line = line.replace(' ','')
        line = line.replace('\n','')
        if(line != ""):
            row = list(eval(line))
            table.append(row)


    file.close()
    dimension = len(table)
    
    print("Data: ")
    for row in table:
        print(row)

    print('''
Dimension: {} x {}
'''.format(dimension,dimension))
    '''
        Input
    '''
    
    Fuzzy_HyperGR_Ideal()
    end()

def implies(x,y):
    truth_value = y if x else True
    print ('      {x} => {y} : {truth_value}'.format(x=x,y=y,truth_value=truth_value))
    return truth_value

def Fuzzy_HyperGR_Ideal():
    global table
    global dimension
    global isHGR
    global isError

    M = []
    for i in range(dimension):
        M.append(eval(input('Enter value of \u03BC({}): '.format(i))))

    print('\n\u03BC: {}'.format(M))
    
    print('''
(i) x << y => \u03BC(y) \u2264 \u03BC(x)
''')

    for x in range(dimension):
        for y in range(dimension):
            print('\n   If x = {} and y = {}:'.format(x,y))
            data = simplify('{x} @ {y}'.format(x=x,y=y))
            print('      {x} << {y} => \u03BC({y}) \u2264 \u03BC({x})'.format(x=x,y=y))
            print('      {zero} \u2286 {data} => {My} \u2264 {Mx}'.format(zero={0},data=data,My=M[y],Mx=M[x]))
            truth_value = implies({0}.issubset(data), M[y] <= M[x])
            
            if(truth_value):
                print('      Check Pass')
            else:
                print('      Check Failed')
                isHGR = False
                end()

                
    print('''
(ii) \u03BC(x) \u2265 min{infu\u2208x@y\u03BC(u),\u03BC(y)}
''')
    for x in range(dimension):
        for y in range(dimension):
            Mx = M[x]
            My = M[y]
            print('\n   If x = {} and y = {}:'.format(x,y))
            print('      \u03BC(x): {}'.format(Mx))
            print('      \u03BC(y): {}'.format(My))
            data = simplify('{x} @ {y}'.format(x=x,y=y))
            print('      x @ y : {}'.format(data) )
            list_data = list(data)
            hold_M = []
            for value in list_data:
                hold_M.append(M[value])
            
            infimum = min(hold_M)
            minimum = min([infimum,My])
            truth_value = Mx >= minimum
            print('      \u03BC(u): {}'.format(hold_M))
            print('      infu\u2208x@y\u03BC(u): {}'.format(infimum))
            print('      min{infu\u2208x@y\u03BC(u),\u03BC(y)}: ' + '{}'.format(minimum))
            print('      {} \u2265 {}: {}'.format(Mx,minimum,truth_value))
            if(truth_value):
                print('      Check Pass')
            else:
                print('      Check Failed')
                isHGR = False
                end()

    print('''
(iii) \u03BC(x) \u2265 min{infv\u2208[(x@z)@z]@(y@z)\u03BC(v),\u03BC(y)}
''')
    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                Mx = M[x]
                My = M[y]
                print('\n   If x = {} and y = {} and z = {}:'.format(x,y,z))
                print('      \u03BC(x): {}'.format(Mx))
                print('      \u03BC(y): {}'.format(My))
                data = simplify('[({x}@{z})@{z}]@({y}@{z})'.format(x=x,y=y,z=z))
                print('      [(x@z)@z]@(y@z) : {}'.format(data) )
                list_data = list(data)
                hold_M = []
                for value in list_data:
                    hold_M.append(M[value])
                
                infimum = min(hold_M)
                minimum = min([infimum,My])
                truth_value = Mx >= minimum
                print('      \u03BC(v): {}'.format(hold_M))
                print('      infv\u2208[(x@z)@z]@(y@z)\u03BC(v): {}'.format(infimum))
                print('      min{infv\u2208[(x@z)@z]@(y@z)\u03BC(v),\u03BC(y)}: ' + '{}'.format(minimum))
                print('      {} \u2265 {}: {}'.format(Mx,minimum,truth_value))
                if(truth_value):
                    print('      Check Pass')
                else:
                    print('      Check Failed')
                    isHGR = False
                    end()
                
            



def simplify(data):
    #print("------------------------------------------->")
    #print("--->Simplifying: ", data)
    #print("------------------------------------------->")
    global table
    global isError
    data = str(data)
    temp = None
    try:
        temp = eval(data)
        
        #remove [] if not necessary
        if type(temp) is list:
            temp = str(data)
            temp = temp.replace('[','').replace(']','')
            simplify(temp)

        return temp  
    except :
        if(type(data) is str):
            if '[' in data:
                start = data.find('[')
                index = start+1
                buffer = 0;
                while index < len(data):
                    if(data[index] == '['):
                        buffer+=1
                    elif(data[index] == ']'):
                        if(buffer == 0):
                            substring = data[start+1:index]
                            substring = simplify(substring)

                            data = data[:start] + str(substring) + data[index+1:]
                            return simplify(data)
                        else:
                            buffer -=1
                    index += 1
            elif '(' in data:
                start = data.find('(')
                index = start+1
                buffer = 0;
                while index < len(data):
                    if(data[index] == '('):
                        buffer+=1
                    elif(data[index] == ')'):
                        if(buffer == 0):
                            substring = data[start+1:index]
                            substring = simplify(substring)

                            data = data[:start] + str(substring) + data[index+1:]
                            return simplify(data)
                        else:
                            buffer -=1
                    index += 1
                    
            elif '@' in data:
                first = set()
                hold_set = set()
                temp = data.split("@")
                i = 0
                #print("Temp: ", temp)
                for x in temp:
                    x = eval(x)
                    if(type(x) is not set):
                        x = {x}

                    #print(x)
                    #print("x type: ", type(x))
                    if i ==0:
                        first = x
                        #print("First :", first)
                    else:
                        #print("-------------------------------------------")
                        #print("Processing {} @ {}".format(first,x))
                        first = list(first)
                        x = list(x)
                        #print(first)
                        for index_first in first:
                            for index_second in x:
                                #print("--->")
                                table_set = table[index_first][index_second]
                                #print("Set of {} @ {} : {}".format(index_first,index_second,table_set))
                                hold_set = hold_set.union(table_set)
                                #print("--->")
                        #print("-------------------------------------------")
                        #print("------------------------------------------->")
                        first = hold_set
                        #print("--->Result of Union: ", hold_set)
                        #print("------------------------------------------->")
                        
                    i += 1
                
                return hold_set

        else:
            isError = True
            end()

def end():
    global isHGR
    global isError
    global fails
    if isError is False:
        print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n")
        if(isHGR == False):
            print("\tData is not a Fuzzy Hyper GR Ideal")
        else:
            print("\tData is a Fuzzy Hyper GR Ideal")
        print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    else:
        print("Ooops Something went wrong...")
        print("Please check your datas")
    print("\n\n\nend of program")
    sys.exit(1)



if __name__== "__main__" :  
    main()
