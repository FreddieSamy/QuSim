class Circuit():
    
    
###############################################################################################################################
    
    #this function takes list of initial states and apply equivalent gates

    #you can intialize your circuit with vector that represent your initialization
    #to initialize two qubits with |1⟩ ... circuit.initialize([0,0,0,1],[0,1])

    #qiskit always start with |0⟩ state
    #|1⟩ state equivalent to X|0⟩
    #|+⟩ state equivalent to H|0⟩
    #|-⟩ state equivalent to H|1⟩ = HX|0⟩
    #|i⟩ = |↻⟩ state equivalent to S|+⟩ = SH|0⟩ = HX|0⟩
    #|-i⟩ = |↺⟩ state equivalent to S|-⟩ = SH|1⟩ = SHX|0⟩ 

    #then this function apply barrier after initial states **we need to check this**

    #dirac notation doc - https://docs.microsoft.com/en-us/quantum/concepts/dirac-notation

    def initState(self,circuit,stateList):
        for i in range(len(stateList)):
            if str(stateList[i])=="1":
                circuit.x(i)
            elif stateList[i]=="+":
                circuit.h(i)
            elif stateList[i]=="-":
                circuit.x(i)
                circuit.h(i)
            elif stateList[i]=="i":
                circuit.h(i)
                circuit.s(i)
            elif stateList[i]=="-i":
                circuit.x(i)
                circuit.h(i)
                circuit.s(i)
        circuit.barrier()
    
    #testing
    """from qiskit import *

    qr=QuantumRegister(6)
    cr=ClassicalRegister(6)
    circuit=QuantumCircuit(qr,cr)

    initState(circuit,["0","1","+","-","i","-i"])

    circuit.h(0)
    circuit.x(0)

    circuit.measure(qr,cr)
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,backend=simulator).result()

    print(circuit)"""


###############################################################################################################################

    #this function applys a matrix (custom gate) to a circuit
    #positions must be list with numbers
    #we must check unitary before storing it 
    #to check unitary use  "is_unitary_matrix(data)"

    def addCustomGate(self,circuit,gateMatrix,postions):
        from qiskit.quantum_info.operators import Operator
        customGate=Operator(gateMatrix)
        circuit.unitary(customGate,postions)
    

    #testing
    """from qiskit import *

    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)
    Matrix=[[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]

    addCustomGate(circuit,Matrix,[0,1])

    circuit.measure(qr,cr)
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,backend=simulator).result()

    %matplotlib inline
    circuit.draw(output='mpl')"""


###############################################################################################################################


    #this function returns dirac notation of the circuit
    #neglects terms with zero probability
    #four digits after floating point

    def diracNotation(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        temp=circuit.copy()
        temp.remove_final_measurements()
    
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(temp,backend=simulator).result()
        statevector=result.get_statevector()
        #print(statevector)
        import math
        diracNotation=""
        for i in range(len(statevector)):
            if statevector[i].real==0 and statevector[i].imag==0:
                continue
            if statevector[i].real!=0:
                if diracNotation!="":
                    if statevector[i].real>0:
                        string="{0:.4f}".format(statevector[i].real).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="+ "+string
                    else:
                        string="{0:.4f}".format(statevector[i].real*-1).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="- "+string
                else:
                    string="{0:.4f}".format(statevector[i].real).replace('.0000','')
                    string="" if abs(float(string))==1 else string
                    diracNotation+=string
                if statevector[i].imag!=0:
                    if statevector[i].imag>0:
                        string="{0:.4f}".format(statevector[i].imag).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="+ "+string+"i"
                    else:
                        string="{0:.4f}".format(statevector[i].imag*-1).replace('.0000','')
                        string="" if abs(float(string))==1 else string
                        diracNotation+="- "+string +" i"
            elif statevector[i].imag!=0:
                if statevector[i].imag>0:
                    string="{0:.4f}".format(statevector[i].imag).replace('.0000','')
                    if float(string)==1:
                        diracNotation+="+ i" if diracNotation!="" else "+ i"
                    else:
                        diracNotation+="+ "+string+" i"
                else:       
                    string="{0:.4f}".format(statevector[i].imag*-1).replace('.0000','')
                    if float(string)==-1:
                        diracNotation+="- i" if diracNotation!="" else "- i"
                    else:
                        diracNotation+="- "+string+" i" 
            
            diracNotation+=" |"+str(("{0:0"+str(int(math.log(len(statevector),2))).replace('.0000','')+"b}").format(i))+"⟩ "
        return diracNotation

    #testing
    """
    from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)

    print(diracNotation(circuit))"""

###############################################################################################################################

    #this function returns readable matrix representation
    #circuit mustn't be measured
    #four digits after floating point
    def matrixRepresentation(self,circuit):
        from qiskit import Aer
        from qiskit import execute

        temp=circuit.copy()
        temp.remove_final_measurements()

        simulator = Aer.get_backend('unitary_simulator')
        result = execute(temp, backend=simulator).result()
        unitary = result.get_unitary()
        #print(unitary)
        matrix=list()
        for i in range(len(unitary)):
            matrix.append(list())
            for j in range(len(unitary[i])):
                matrix[i].append
                if unitary[i][j].real==0 and unitary[i][j].imag==0:
                    matrix[i].append("0")
                if unitary[i][j].real!=0:
                    matrix[i].append(str("{0:.4f}".format(unitary[i][j].real)).replace('.0000',''))
                    if unitary[i][j].imag!=0:
                        matrix[i][j]+="+"+str("{0:.4f}".format(unitary[i][j].imag).replace('.0000',''))+" i"
                elif unitary[i][j].imag!=0:
                    matrix[i].append(str("{0:.4f}".format(unitary[i][j].imag)+" i").replace('.0000',''))
            
        return matrix

    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)


    print("Matrix Representation before measurement")
    print(matrixRepresentation(circuit))"""

###############################################################################################################################

    #displays matrix with mathimatical format
    
    def matrixLatex(self,matrix):
        from IPython.display import display, Markdown
        gate_latex = '\\begin{pmatrix}'
        for line in matrix:
            for element in line:
                gate_latex += str(element) + '&'
            gate_latex  = gate_latex[0:-1]
        
            gate_latex +=  ' \\\\ '
        gate_latex  = gate_latex[0:-4]
        gate_latex += '\end{pmatrix}'
        return display(Markdown(gate_latex))


    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)

    print("Matrix Representation before measurement")
    matrixLatex(matrixRepresentation(circuit))"""

###############################################################################################################################

    def matrixRepresentation2(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        
        temp=circuit.copy()
        temp.remove_final_measurements()
    
        backend = Aer.get_backend('unitary_simulator')
        gate = execute(temp,backend).result().get_unitary()

        from IPython.display import display, Markdown
        gate_latex = '\\begin{pmatrix}'
        for line in gate:
            for element in line:
                gate_latex += str(element) + '&'
            gate_latex  = gate_latex[0:-1]
            gate_latex +=  '\\\\ '
        gate_latex  = gate_latex[0:-4]
        gate_latex += '\end{pmatrix}'
        return display(Markdown(gate_latex))

    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)


    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)

    print("Matrix Representation before measurement")
    matrixRepresentation2(circuit)"""

###############################################################################################################################

    #this function returns counts of all states
    #we can use this data to draw a plot histogram with probabilities
    #plot_histogram(graphData(circuit,numberOfShots))
    #divide all counts by number of shots to get probabilities 
    def graphData(self,circuit,numberOfShots):
        from qiskit import Aer
        from qiskit import execute
        
        simulator=Aer.get_backend('qasm_simulator')
        result=execute(circuit,backend=simulator,shots=numberOfShots).result()
        
        return result.get_counts(circuit)

    #testing 
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)

    circuit.x(0)
    circuit.cx(0,1)
    
    circuit.measure(qr,cr)
    
    from qiskit.tools.visualization import plot_histogram
    plot_histogram(graphData(circuit,1024*2))"""

###############################################################################################################################

    #drawing of the circuit
    def draw(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        
        simulator=Aer.get_backend('qasm_simulator')
        execute(circuit,backend=simulator).result()
        #%matplotlib inline
        return circuit.draw(output='mpl')

    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)

    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)
    draw(circuit)"""

###############################################################################################################################

    #function to draw bloch spheres of the circuit
    def blochSphere(self,circuit):
        from qiskit import Aer
        from qiskit import execute
        from qiskit.visualization import plot_bloch_multivector
        simulator=Aer.get_backend('statevector_simulator')
        result=execute(circuit,backend=simulator).result()
        statevector=result.get_statevector()
        return plot_bloch_multivector(statevector)


    #testing
    """from qiskit import *
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)

    circuit.x(0)
    circuit.cx(0,1)

    circuit.measure(qr,cr)
    blochSphere(circuit)"""
    
    
###############################################################################################################################
    
    
    #we have to check this with multiple users 
    #it saves API_TOKEN locally 
    def runOnIBMQ(self,API_TOKEN,circuit,shots):
        from qiskit import IBMQ
        from qiskit import execute
        IBMQ.save_account(API_TOKEN)
        IBMQ.load_account()
        provider=IBMQ.get_provider('ibm-q')
        qcomp=provider.get_backend('ibmq_16_melbourne')
        job=execute(circuit,backend=qcomp,shots=shots)
        return job

    #testing
    """API_TOKEN=""
    
    qr=QuantumRegister(2)
    cr=ClassicalRegister(2)
    circuit=QuantumCircuit(qr,cr)
    circuit.h(0)
    circuit.cx(0,1)

    job=runOnIBMQ(API_TOKEN,circuit)

    print("https://quantum-computing.ibm.com/results/"+job.job_id())

    #from qiskit.tools.monitor import job_monitor
    #job_monitor(job)"""

###############################################################################################################################
    
    def singleQubitGates(self,circuit,column,customGates):
        for i in range(len(column)):
            if str(column[i])=="":
                continue
            if str(column[i])[:7]=="custom_":
                if customGates==None:
                    print("send custom gates")
                else:
                    gateName=str(column[i])[7:]
                    if len(customGates[gateName])==2:
                        self.addCustomGate(circuit,customGates[gateName],[i])
                        continue
                    else:
                        self.multiQubitGates(circuit,column,customGates)
                        continue
            pythonLine="circuit."+column[i]+"("
            pythonLine+=str(i)
            pythonLine+=")"
            #print(pythonLine)
            exec(pythonLine)


###############################################################################################################################

    def multiQubitGates(self,circuit,column,customGates):
        c=[]
        oc=[]
        swap=[]
        controlledGates=[]
        customPos={}
        for i in range(len(column)):
            if str(column[i])=="":
                continue
            
            if str(column[i])=="c":
                c.append(str(i))
                
            elif str(column[i])=="oc":
                oc.append(str(i))
                c.append(str(i))
                
            elif str(column[i])=="swap":
                swap.append(i)
                
            elif str(column[i])[:7]=="custom_" :
                gateName=str(column[i])[7:]
                if customGates==None:
                    print("send custom gates")
                else:
                    if gateName in customPos.keys():
                        customPos[gateName].append(i)
                    else:
                        customPos[gateName]=[i]
                
            else:
                controlledGates.append([column[i],str(i)])
            
        
        if len(c)==0:
            
            if len(swap)!=0:                                  #swap
                circuit.swap(swap[0],swap[1])
                column[swap[0]]=""
                column[swap[1]]=""
            
            if len(customPos)!=0:                             #custom gates
                for i in customPos:
                    print(customGates[i],customPos[i])
                    self.addCustomGate(circuit,customGates[i],customPos[i])
                    for j in customPos[i]:
                        column[j]=""
                
            self.singleQubitGates(circuit,column,customGates)
            
        else:
            
        
            for i in oc:                                       #open control 
                circuit.x(int(i))
            
            if len(swap)!=0:                                   #cswap
                circuit.cswap(int(c[0]),swap[0],swap[1])
             
            ##if len(customPos)!=0:                            #controlled custom gates
            ## what should we do ?!!
                
                                                               #controlled gates
            cStr=",".join(c)
            for i in controlledGates:
                pythonLine="circuit."+"c"*len(c)+i[0]+"("+cStr+","+i[1]+")"
                #print(pythonLine)
                exec(pythonLine)    
        
                
            for i in oc:                                        #open control 
                circuit.x(int(i))
            
        
###############################################################################################################################


    #main function
    #takes json object that represent a circuit
    #returns json object with all results
    
    #this functions applies only single qubit gates "till now"
    #"cols" in received json object is mandatory to get results
    #default number of shots is 1024
    #to run a circuit on IBMQ , "API_TOKEN" must be sent 
    #to initialize the circuit , "init" must be sent as a vector ( i.e. [0,1,"+","-","i","-i"] )
    
    def createCircuit(self,circuit,receivedDictionary):
        
        shots=1024
        returnedDictionary={}
        customGates=None
    
        if "shots" in receivedDictionary:
            shots=receivedDictionary["shots"]
            
        if "custom" in receivedDictionary:
            customGates=receivedDictionary["custom"]
        
        if "cols" in receivedDictionary:
            matrix=receivedDictionary["cols"]
            columns=len(matrix)
        
            if "init" in receivedDictionary:
                self.initState(circuit,receivedDictionary["init"])
    
            for i in range(columns): #number of columns 
                if "swap" in matrix[i] or "c" in matrix[i] or "oc" in matrix[i]:
                    self.multiQubitGates(circuit,matrix[i],customGates)
                elif "barrier" in matrix[i]:
                    circuit.barrier()
                else:
                    self.singleQubitGates(circuit,matrix[i],customGates)
        
            circuit.measure_all()
        
            #print(circuit)
        
            if "API_TOKEN" in receivedDictionary:
                job=self.runOnIBMQ(receivedDictionary["API_TOKEN"],circuit,shots)
            
                returnedDictionary={"diracNotation":self.diracNotation(circuit),
                                    "matrixRepresentation":self.matrixRepresentation(circuit),
                                    "qasm":circuit.qasm(),
                                    "link":"https://quantum-computing.ibm.com/results/"+job.job_id()
                                   }
            
                #we cannot get results until the job is completed
                #from qiskit.tools.monitor import job_monitor
                #job_monitor(job)
                #result=job.result()
                #result.get_counts(circuit)
        
            else:
                returnedDictionary={"diracNotation":self.diracNotation(circuit),
                                    "matrixRepresentation":self.matrixRepresentation(circuit),
                                    "qasm":circuit.qasm(),
                                    "graphData":self.graphData(circuit,shots),
                                    "shots":shots
                                   }
    
        return returnedDictionary

    #testing
    #from qiskit import circuit

    #run on simulator
    """dic={
     "wires":6,
     "cols":[["h"],
             ["x"],
             ["y"],
             ["z"],
             ["s"],
             ["sdg"],
             ["t"],
             ["tdg"],
             ["barrier"],
             ["","c","h"],
             ["","c","x"],
             ["","c","y"],
             ["","c","z"],
             ["","oc","h"],
             ["","oc","x"],
             ["","oc","y"],
             ["","oc","z"],
             ["","swap","swap"],
             ["barrier"],
             ["","","","c","c","x"],
             ["","","","c","swap","swap"],
             ["","","","oc","oc","x"],
             ["","","","oc","swap","swap"],
             ["barrier"],
             ["","","","","","custom_not"],
             ["","","","custom_I4","","custom_I4"]],
     "init":[0,1,"+","-","i","-i"],
     "shots":2048,
     "custom":{
               "not":[[0,1],[1,0]],
               "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
               }
     }
     
    createCircuit(dic)"""

    #run on IBMQ
    """dic={
     "wires":6,
     "cols":[["h"],
             ["x"],
             ["y"],
             ["z"],
             ["s"],
             ["sdg"],
             ["t"],
             ["tdg"],
             ["barrier"],
             ["","c","h"],
             ["","c","x"],
             ["","c","y"],
             ["","c","z"],
             ["","oc","h"],
             ["","oc","x"],
             ["","oc","y"],
             ["","oc","z"],
             ["","swap","swap"],
             ["barrier"],
             ["","","","c","c","x"],
             ["","","","c","swap","swap"],
             ["","","","oc","oc","x"],
             ["","","","oc","swap","swap"],
             ["barrier"],
             ["","","","","","custom_not"],
             ["","","","custom_I4","","custom_I4"]],
     "init":[0,1,"+","-","i","-i"],
     "shots":2048,
     "custom":{
               "not":[[0,1],[1,0]],
               "I4":[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
               }
     }
    
    createCircuit(dic)"""
    
###############################################################################################################################

###############################################################################################################################

###############################################################################################################################
