#pip install qiskit

# https://www.youtube.com/watch?v=yGzmA98D0eU

import qiskit as q
import matplotlib.pyplot as plt

# here we use a quantum computer simulator - with no access to underlying vectors

# init quantum computer simulator
simulator = q.Aer.get_backend('qasm_simulator')

# init circuit
circuit = q.QuantumCircuit(1,1) #qbits, classic measure bits

# build circuit
#  add hadamard gate on line 0
circuit.h(0)
#  add measure of qbit line 0 to classic line 0 - to enable counts
circuit.measure(0,0)

# display circuit
print(circuit.draw(output='text'))

# run circuit on simulator
job = q.execute(circuit, simulator, shots=1000)

# wait for results
result = job.result()

# count measures
counts = result.get_counts(circuit)
print(f"Nombre de 0 et 1:{counts}")

# display results
q.visualization.plot_histogram(counts)
plt.show()

# EOF