
state = {}

class program(object):

    def __init__(self,lines):
        self.lines = lines
            

    def eval(self):
        i = 0
        #print(self.lines)
        while i < len(self.lines):
            if 'print' in self.lines[i]:
                pos = self.lines[i].find('t')
                disp_inst = display(self.lines[i][pos+2:])
                disp_inst.eval()
                i += 1
                continue
            elif 'while' in self.lines[i]:
                #print('i=',i)
                pos = self.lines[i].find('e')
                while_inst = condition()
                if(while_inst.eval(self.lines[i][pos+1:(len(self.lines[i])-3)])):
                    #print("!!")
                    cwhile = 0
                    cdone = 0
                    for j in range(i,len(self.lines)):
                        if 'while' in self.lines[j]:
                            cwhile += 1
                        if 'done' in self.lines[j]:
                            cdone += 1
                        if cwhile == cdone:
                            break
                    p = program(self.lines[i+1:j])
                    p.eval()
                    continue
                else:
                    cwhile = 0
                    cdone = 0
                    for j in range(i,len(self.lines)):
                        if 'while' in self.lines[j]:
                            cwhile += 1
                        if 'done' in self.lines[j]:
                            cdone += 1
                        if cwhile == cdone:
                            break
                    i = j + 1
                    continue
            elif 'if' in self.lines[i]:
                pos = self.lines[i].find('f')
                if_inst = condition()
                if(if_inst.eval(self.lines[i][pos+1:(len(self.lines[i])-1)])):
                    #print("if true!!")
                    cif = 0
                    cfi = 0
                    for j in range(i,len(self.lines)):
                        if 'if' in self.lines[j]:
                            cif += 1
                        if 'fi' == self.lines[j]:
                            cfi += 1
                        if cif == cfi:
                            break
                    cif = 0
                    celse = 0
                    flag = 0
                    for k in range(i,len(self.lines)):
                        if 'if' in self.lines[k]:
                            cif += 1
                        if 'else' == self.lines[k]:
                            celse += 1
                        if cif == celse:
                            flag = 1
                            break
                    if flag == 1:
                        p = program(self.lines[i+2:k])
                        p.eval()
                    else:
                        p = program(self.lines[i+2:j])
                        p.eval()
                    i = j+1
                else:
                    #print("else true!!")
                    cif = 0
                    cfi = 0
                    for j in range(i,len(self.lines)):
                        if 'if' in self.lines[j]:
                            cif += 1
                        if 'fi' == self.lines[j]:
                            cfi += 1
                        if cif == cfi:
                            break
                    cif = 0
                    celse = 0
                    flag = 0
                    for k in range(i,len(self.lines)):
                        if 'if' in self.lines[k]:
                            cif += 1
                        if 'else' == self.lines[k]:
                            celse += 1
                        if cif == celse:
                            flag = 1
                            break
                    if flag == 1:
                        i = k+1
                    else:
                        i = j+1
                continue
            
            elif 'fi' == self.lines[i]:
                i += 1
                continue

            elif ':=' in self.lines[i]:
                pos = self.lines[i].find(':=')
                assgn_inst = assgn_stmt()
                assgn_inst.eval(self.lines[i][0:pos],self.lines[i][pos+2:])
                #print(state)
                i += 1
                continue
            else:
                raise Exception('Syntax Error in line ' + str(i+1))

            

class condition(object):

    def eval(self,cond):
        
        if '<=' in cond:
            pos = cond.find('<')
            left_exp = expression()
            left = left_exp.eval(cond[:pos])
            right_exp = expression()
            right = right_exp.eval(cond[pos+2:])
            #print('left=',left)
            #print('right=',right)
            if float(left) <= float(right):
                return True
            else:
                return False

        elif '>=' in cond:
            pos = cond.find('>')
            left_exp = expression()
            left = left_exp.eval(cond[:pos])
            right_exp = expression()
            right = right_exp.eval(cond[pos+2:])
            #print('left=',left)
            #print('right=',right)
            if float(left) >= float(right):
                return True
            else:
                return False

        elif '<' in cond:
            pos = cond.find('<')
            left_exp = expression()
            left = left_exp.eval(cond[:pos])
            right_exp = expression()
            right = right_exp.eval(cond[pos+1:])
            #print('left=',left)
            #print('right=',right)
            if float(left) < float(right):
                return True
            else:
                return False

        elif '>' in cond:
            pos = cond.find('>')
            left_exp = expression()
            left = left_exp.eval(cond[:pos])
            right_exp = expression()
            right = right_exp.eval(cond[pos+1:])
            #print('left=',left)
            #print('right=',right)
            if float(left) > float(right):
                return True
            else:
                return False

        elif '==' in cond:
            pos = cond.find('=')
            left_exp = expression()
            left = left_exp.eval(cond[:pos])
            right_exp = expression()
            right = right_exp.eval(cond[pos+2:])
            #print('left=',left)
            #print('right=',right)
            if float(left) == float(right):
                return True
            else:
                return False

        elif '!=' in cond:
            pos = cond.find('!')
            left_exp = expression()
            left = left_exp.eval(cond[:pos])
            right_exp = expression()
            right = right_exp.eval(cond[pos+2:])
            #print('left=',left)
            #print('right=',right)
            if float(left) != float(right):
                return True
            else:
                return False




class assgn_stmt(object):

    def eval(self,var_name=None,value=None):
        exp_inst = expression()
        state[var_name] = exp_inst.eval(value)


class expression(object):

    def eval(self,ex):            
        #print(ex)
        flag=0
        count=0
        check=0
        for i in range(0,len(ex)):
            l=[]
            r=[]
            check = 0
            if(ex[i] == '+' or ex[i] == '*' or ex[i] == '-' or ex[i] == '/'):
                l=ex[:i]
                r=ex[i+1:]
                c1=0
                c2=0
                for j in l:
                    if(j=="("):
                        c1+=1
                    if(j==")"):
                        c2+=1
                if c1==c2:
                    check +=1
                c1=0
                c2=0
                for j in r:
                    if(j=="("):
                        c1+=1
                    if(j==")"):
                        c2+=1
                if c1==c2:
                    check += 1
                
                if check==2:
                    flag=1
                    break
        
            
        if (flag==0):    
            if(ex[:].isalpha()): 
                return state[ex[:]]
            elif(ex[:].isnumeric()):
                return int(ex[:])
                    
        
        if(ex[i-1]==")"):
            #print("hi"+ex[:i]+str( i))
            for j in range(i-1,-1,-1):
                if ex[j] == "(":
                    break
            #print(ex[j:i] + "ooolALALA")
            exp1=expression()
            left =exp1.eval(ex[j+1:i-1])
        else:
            left = ex[0:i] 
        if(ex[i+1]=="("):
            for j in range(i+2,len(ex)):
                if ex[j] == ")":
                    break
            exp1=expression()
            
            right=exp1.eval(ex[i+2:j])
        else:
            right = ex[i+1:]

        #print("ghjgh"+" "+str((right)))
        #print("vbvbn"+str(left))

        if(left.isalpha()):
            #print("yes"+ state[left])
            left =float(state[left])
        else:
            #print("hii"+str(left))
            left = float(left)
        if(right.isalpha()):
            
            right = float(state[right])
        else:
            #print("hiii"+str(right))
            right = float(right)

        if ex[i]=="+":
            #print("hiiii")
            return str(left + right)
        elif ex[i]=="*":
            return str(left * right)
        elif ex[i]=='-':
            return str(left-right)
        elif ex[i]=='/':
            return str(left/right)


class variable(object):
    
    def __init__(self,var_name=None,var_value=None):
        
        self.name = var_name
        self.value = var_value
        state[var_name] = var_value

    def eval(self):
        
        return state[self.name]


class integer(object):

    def __init__(self,integer):

        self.value = int(integer)

    def eval(self):

        return self.value

class display(object):

    def __init__(self,toprint):
        self.toprint = toprint

    def eval(self):
        if self.toprint[0] == '"':
            print(self.toprint[1:(len(self.toprint)-1)],end=' ')
            return
        
        elif self.toprint == r'\n':
            print('\n',end=' ')
            return

        else:
            exp_inst = expression()
            print(exp_inst.eval(self.toprint),end=' ')


fp = open('test.txt')
stmts = []
no_of_lines = sum(1 for _ in fp)
fp.seek(0)
#stmts = [fp.readline().split() for i in range(no_of_lines)]
stmts = [fp.readline().strip('\n') for i in range(no_of_lines)]
for i in range(len(stmts)):
    if stmts[i][len(stmts[i])-1] != ';' and stmts[i].find('while') != 0 and stmts[i].find('if') != 0:
        raise Exception('Syntax Error in line ' + str(i+1)) 
    if 'print' in stmts[i]:
        continue
    else:
        stmts[i]=stmts[i].replace(' ','')
        #print(stmts[i])

stmts = [s.strip(';') for s in stmts]
#print(stmts)
pro = program(stmts)
#pro.eval()
try:    
    pro.eval()
except Exception as e:
    print("Syntax Error!!")
#print('\n')
#print("@@",state,"@@")