
#!python3

import matplotlib.pyplot as plt
import qiskit as q

# here we use a quantum computer simulator - with no access to underlying vectors
# init quantum computer simulator
simulator = q.Aer.get_backend('qasm_simulator')

# init circuit
circuit = q.QuantumCircuit(2,2) #qbits, classic measure bits

# build circuit
circuit.h(0) #Hadamard line 0
circuit.x(0) #Pauly X (invert |0> and |1> )
circuit.cx(0,1) #CNOT 0-1
circuit.h(1) #Hadamard line 1
#  add measure of qbit line 0 & 1 to classic lines 0 & 1 - to enable counts
# circuit.measure([0,1],[0,1])
circuit.measure_all()

# display circuit in mpl
print(circuit.draw('mpl'))

# display circtuit in ascii
print(circuit.draw())

# run circuit on simulator
job = q.execute(circuit, simulator, shots=1000)

# wait for results
result = job.result()

# count measures
counts = result.get_counts(circuit)
print(f"Counts:{counts}")

# display results
q.visualization.plot_histogram(counts)
plt.show()