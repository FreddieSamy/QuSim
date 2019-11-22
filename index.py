from functions import Circuit
from qiskit import QuantumCircuit


dic={
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

if "cols" in dic and "wires" in dic:    
    circuit=QuantumCircuit(dic["wires"])
    #circuit.cswap(0,1,2)
    c=Circuit()
    
    print(c.createCircuit(circuit,dic))
    print(circuit)