#!python3

import os
from dotenv import load_dotenv
import qiskit as q
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import plot_histogram
import qiskit_ibm_runtime
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import Session, Options, Sampler

#Check jobs on web console
# https://quantum-computing.ibm.com/jobs

print(qiskit_ibm_runtime.version.get_version_info())

# Load API Key
def loadapikey():
    load_dotenv()  # take environment variables from .env.
    qiskit_api_key = os.environ.get("QISKIT_IBM_TOKEN")
    assert qiskit_api_key is not None
    return qiskit_api_key

# Connect to ibm quantum service
def initservice(qiskit_api_key):
    service = QiskitRuntimeService(channel="ibm_quantum", token=qiskit_api_key)
    if False:
        # Optional - save credentials to disk
        try:
            QiskitRuntimeService.save_account(channel="ibm_quantum", token=quiskit_api_key)
        except:
            print("Account info already saved")
        # Then you can login without args
        service = QiskitRuntimeService()
    # display current supported backends
    backends = service.backends()
    print(f'backends: {", ".join(list(map(lambda b : b.name,backends)))}')
    return service

service = initservice(loadapikey())

def runhelloworld(service):
    # basic test on simulator backend
    backend = service.least_busy(simulator=True, operational=True).name
    print(f"least_busy simulator backend: {backend}")
    options = {"backend": backend}
    program_inputs = {"iterations": 1}
    job = service.run(program_id="hello-world", options=options, inputs=program_inputs)
    print(f"job id: {job.job_id()}")
    #job_monitor(job,interval=10)
    result = job.result()
    print(result)

runhelloworld(service)

def preparebellcircuit():
    # init & build circuit
    circuit = q.QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    print(circuit.draw())
    return circuit

bell = preparebellcircuit()

def getlazybackend(service):
    # Ask IBM Quantum for its least busy device that isn't a simulator.
    backend = service.least_busy(simulator=False, operational=True)
    print(f'least_busy real backend: {backend.name}')
    return backend

backend = getlazybackend(service)

def runcircuit(service,backend,circuit):
    options = Options(optimization_level=1)
    options.execution.shots = 1024  # Options can be set using auto-complete.
    print(f"backend: {backend.name}")
    session = Session(service=service, backend=backend.name)
    sampler = Sampler(session=session, options=options)
    job = sampler.run(circuits=circuit)
    print(f"job_id: {job.job_id()}")
    # monitor job submission
    #job_monitor(job,interval=10)
    # wait for results
    result = job.result()
    print(f"Job result: {result}")
    # count measures
    counts = result.quasi_dists[0].binary_probabilities()
    print(f"Counts: {counts}")
    # Plot the results
    plot_histogram(result.quasi_dists[0].binary_probabilities(), title="bell")

runcircuit(service,backend,bell)