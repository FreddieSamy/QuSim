from functions import Circuit
from qiskit import QuantumCircuit


dic={"wires":6,
     "cols":[["h"],
             ["x"],
             ["y"],
             ["z"],
             ["s"],
             ["sdg"],
             ["t"],
             ["tdg"],
             ["","c","h"],
             ["","c","x"],
             ["","c","y"],
             ["","c","z"],
             ["","oc","h"],
             ["","oc","x"],
             ["","oc","y"],
             ["","oc","z"],
             ["","swap","swap"],
             ["","","","c","c","x"],
             ["","","","c","swap","swap"],
             ["","","","oc","oc","x"],
             ["","","","oc","swap","swap"]],
     "init":[0,1,"+","-","i","-i"],
     "shots":1024*2}

if "cols" in dic:    
    circuit=QuantumCircuit(dic["wires"])
    #circuit.cswap(0,1,2)
    c=Circuit()
    
    print(c.createCircuit(circuit,dic))
    print(circuit)