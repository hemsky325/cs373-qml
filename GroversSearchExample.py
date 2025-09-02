# grovers_search.py
#
# This script implements Grover's algorithm, a quantum algorithm for unstructured
# search. This example finds the state |11> in a 2-qubit system.

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

# --- Helper function to create the diffuser ---
def diffuser(nqubits):
    """Creates the Grover diffuser circuit for n qubits."""
    qc = QuantumCircuit(nqubits)
    # Apply Hadamard to all qubits
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply X to all qubits
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply multi-controlled Z gate
    qc.h(nqubits - 1)
    qc.mct(list(range(nqubits - 1)), nqubits - 1)  # Multi-controlled Toffoli
    qc.h(nqubits - 1)
    # Apply X to all qubits
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply Hadamard to all qubits
    for qubit in range(nqubits):
        qc.h(qubit)
    # Return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "Diffuser"
    return U_s

# --- Main script ---
# 1. Define the search space size (number of qubits)
n = 2
# The state we want to find
marked_state = '11'

# 2. Create the Oracle for the marked state |11>
# The oracle "marks" the solution by flipping its phase.
# For |11>, a controlled-Z gate does this perfectly.
oracle = QuantumCircuit(n, name="Oracle")
oracle.cz(0, 1) # Flips the phase of |11>
oracle_gate = oracle.to_gate()

# 3. Build the main Grover circuit
grover_circuit = QuantumCircuit(n, n)

# 4. Start with a uniform superposition
grover_circuit.h(range(n))
grover_circuit.barrier()

# 5. Determine the optimal number of iterations
# For N items (2^n), the optimal number is approx. (pi/4)*sqrt(N)
iterations = int(np.floor(np.pi / 4 * np.sqrt(2**n)))
print(f"Number of qubits: {n}")
print(f"Marked state: |{marked_state}>")
print(f"Optimal number of Grover iterations: {iterations}")

# 6. Apply Grover's algorithm (Oracle + Diffuser) for the optimal number of times
for _ in range(iterations):
    grover_circuit.append(oracle_gate, [0, 1])
    grover_circuit.append(diffuser(n), range(n))
    grover_circuit.barrier()

# 7. Measure the qubits
grover_circuit.measure(range(n), range(n))

# 8. Draw the circuit
print("\nGrover's Search Circuit:")
print(grover_circuit.draw())

# 9. Simulate the circuit
simulator = AerSimulator()
compiled_circuit = transpile(grover_circuit, simulator)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()
counts = result.get_counts(grover_circuit)

# 10. Print and plot the results
print("\nSimulation Results:")
print(counts)
# The result should show a high probability of measuring the marked state '11'.
plot = plot_histogram(counts, title="Grover's Search Results")
try:
    plot.show()
except Exception as e:
    print(f"\nCould not display plot. You may need to run 'plot.show()'. Error: {e}")
