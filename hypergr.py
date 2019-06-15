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
    hgr1()
    hgr2()
    hgr3()
    hgr4()
    hgr5()
    end()

def hgr1():
    global table
    global dimension
    global isHGR
    global isError
    
    print('''
Solving HGR1: ( x @ z ) @ ( y @  z ) << x @ y
''')
    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                print('\n   If x = {} and y = {} and z = {}:'.format(x,y,z))
                equation = '( {x} @ {z} ) @ ( {y} @  {z} ) << {x} @ {y}'.format(x=x,y=y,z=z)
                hold = equation.split('<<')
                first = simplify(hold[0])
                second = simplify(hold[1])
                data = simplify('{a} @ {b}'.format(a=first,b=second))
                print('      {}'.format(equation))
                print('      {first} @ {second} => {data}'.format(first=first,second=second,data=data))
                if({0}.issubset(data)):
                    print('      Check Pass')
                else:
                    print('      Check Failed')
                    isHGR = False
                    isError = False
                    end()


def hgr2():
    global table
    global dimension
    global isHGR
    global isError
    
    print('''
Solving HGR2: ( x @ y ) @ z = ( x @ z ) @ y
''')
    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                print('\n   If x = {} and y = {} and z = {}:'.format(x,y,z))
                equation = '( {x} @ {y} ) @ {z} = ( {x} @ {z} ) @ {y}'.format(x=x,y=y,z=z)
                hold = equation.split('=')
                first = simplify(hold[0])
                second = simplify(hold[1])
                print('      {}'.format(equation))
                truth_value = first == second
                print('      {} = {}: {}'.format(first,second,truth_value))
                if(truth_value):
                    print('      Check Pass')
                else:
                    print('      Check Failed')
                    isHGR = False
                    isError = False
                    end()
def hgr3():
    global table
    global dimension
    global isHGR
    global isError
    print('''
Solving HGR3: x << x
''')
    for x in range(dimension):
        print('   If x = {}: '.format(x))
        equation = '{x} << {x}'.format(x=x)
        hold = equation.split('<<')
        first = simplify(hold[0])
        second = simplify(hold[1])
        data = simplify('{x} @ {x}'.format(x=x))
        print('      {x} @ {x} => {data}'.format(x=x,data=data))
        if({0}.issubset(data)):
            print('      Check Pass')
        else:
            print('      Check Failed')
            isHGR = False
            isError = False
            end()
            
def hgr4():
    global table
    global dimension
    global isHGR
    global isError
    print('''
Solving HGR4: 0 @ ( 0 @ x ) << x , x != 0
''')
    for x in range(1,dimension):
        print('   If x = {}: '.format(x))
        equation = '0 @ ( 0 @ {x} ) << {x}'.format(x=x)
        hold = equation.split('<<')
        first = simplify(hold[0])
        second = simplify(hold[1])
        data = simplify('{first} @ {second}'.format(first=first,second=second))
        print('      {}'.format(equation))
        print('      {first} @ {second} => {data}'.format(first=first,second=second,data=data))
        if({0}.issubset(data)):
            print('      Check Pass')
        else:
            print('      Check Failed')
            isHGR = False
            isError = False
            end()

def hgr5():
    global table
    global dimension
    global isHGR
    global isError
    
    print('''
Solving HGR5: ( x @ y ) @ z << y @ z
''')
    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                print('\n   If x = {} and y = {} and z = {}:'.format(x,y,z))
                equation = '( {x} @ {y} ) @ {z} << {y} @ {z}'.format(x=x,y=y,z=z)
                hold = equation.split('<<')
                first = simplify(hold[0])
                second = simplify(hold[1])
                data = simplify('{a} @ {b}'.format(a=first,b=second))
                print('      {}'.format(equation))
                print('      {first} @ {second} => {data}'.format(first=first,second=second,data=data))
                if({0}.issubset(data)):
                    print('      Check Pass')
                else:
                    print('      Check Failed')
                    isHGR = False
                    isError = False
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
            print("\tData is not a Hyper GR")
        else:
            print("\tData is a Hyper GR")
        print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    else:
        print("Ooops Something went wrong...")
        print("Please check your datas")
    print("\n\n\nend of program")
    sys.exit(1)



if __name__== "__main__" :  
    main()
