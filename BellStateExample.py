# bell_state.py
#
# This script demonstrates the creation of a Bell state, which is a fundamental
# example of quantum entanglement and superposition.

# 1. Import necessary libraries from Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# 2. Create a quantum circuit with 2 qubits and 2 classical bits
# Qubits are for quantum operations, classical bits are for storing measurement results.
qc = QuantumCircuit(2, 2)

# 3. Apply the gates to create the Bell state (|00> + |11>)/sqrt(2)
# Apply a Hadamard gate to the first qubit (q0) to put it in superposition.
qc.h(0)
# Apply a CNOT gate with q0 as the control and q1 as the target to entangle them.
qc.cx(0, 1)

# 4. Measure the qubits
# The result of measuring qubit 0 is stored in classical bit 0, and qubit 1 in classical bit 1.
qc.measure([0, 1], [0, 1])

# 5. Draw the circuit to visualize it
print("Quantum Circuit for Bell State:")
print(qc.draw())

# 6. Run the simulation
# Use the AerSimulator to execute the circuit.
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
job = simulator.run(compiled_circuit, shots=1024) # Run the circuit 1024 times

# 7. Get and display the results
result = job.result()
counts = result.get_counts(qc)
print("\nSimulation Results:")
print(counts)

# In an ideal simulation, you will see roughly 50% of the measurements as '00'
# and 50% as '11', demonstrating the entanglement. You will never see '01' or '10'.

# 8. Plot the results as a histogram
# This requires matplotlib to be installed (`pip install matplotlib`)
print("\nPlotting results...")
plot = plot_histogram(counts, title='Bell State Measurement Results')
# To display the plot, you might need to call plot.show() if not in an interactive environment
try:
    plot.show()
except Exception as e:
    print(f"Could not display plot. You may need to run 'plot.show()'. Error: {e}")
