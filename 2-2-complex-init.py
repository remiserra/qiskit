#!python3

# https://www.youtube.com/watch?v=7tO15IFNtMQ

import numpy as np
import qiskit as q
import matplotlib.pyplot as plt
import greeksymbols

# here we use a quantum vector simulator, with access to underlying vectors info

# init simulator - of quantic state
simulator = q.Aer.get_backend('statevector_simulator')

# init circuit
circuit = q.QuantumCircuit(1)  # qbits, no measure bits


def getnorm(l):
    squaresum = np.sum(np.abs(l)**2)
    return np.sqrt(squaresum)


# init starting qbit : α |O> + β |1>
alpha0 = 3+1j
beta0 = 1-2j
# norm = np.sqrt(abs(alpha0)**2 + abs(beta0)**2)
norm = getnorm([alpha0,beta0])
alpha, beta = alpha0/norm, beta0/norm
startstate = [alpha, beta]
print(f"|{greeksymbols.alpha}|:{abs(alpha)**2}")
print(f"|{greeksymbols.beta}|:{abs(beta)**2}")
print(f"Input vector: {startstate}")

# init circuit qbit
startqbit = q.extensions.Initialize(startstate)
circuit.append(startqbit, [0])  # init qbit on quantum line 0

# build circuit
circuit.x(0)

# display circuit
print(circuit.draw(output='text'))

# run circuit on simulator
job = q.execute(circuit, simulator)

# wait for results
result = job.result()

# get result vector (alpha, beta)
endstate = result.get_statevector()
print(f"Output vector: {endstate}")

# count
counts = result.get_counts(circuit)
print(f"Nombre de 0 et 1:{counts}")

# display results
q.visualization.plot_histogram(counts)
plt.show()

# EOF
