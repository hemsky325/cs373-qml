# quantum_teleportation.py
#
# This script demonstrates the quantum teleportation protocol, which allows
# transferring the state of a qubit from one location to another using
# entanglement and classical communication.

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import random_statevector

# --- Setup ---
# Create the registers
# q_source is the qubit whose state we want to teleport
q_source = QuantumRegister(1, name="source")
# q_entangled is the entangled pair shared between sender (Alice) and receiver (Bob)
q_entangled = QuantumRegister(2, name="epr")
# c_classical is for classical communication
c_classical = ClassicalRegister(2, name="classical_bits")

# Create the main circuit
qc = QuantumCircuit(q_source, q_entangled, c_classical)

# --- Step 1: Create an initial state to teleport ---
# Let's create a random quantum state for our source qubit.
random_ket = random_statevector(2)
qc.initialize(random_ket, q_source[0])
qc.barrier()

# --- Step 2: Create an entangled Bell pair ---
# This pair will be shared between the sender and receiver.
# The sender has q_entangled[0], and the receiver has q_entangled[1].
qc.h(q_entangled[0])
qc.cx(q_entangled[0], q_entangled[1])
qc.barrier()

# --- Step 3: Sender's operations ---
# The sender (Alice) interacts the source qubit with her half of the entangled pair.
qc.cx(q_source[0], q_entangled[0])
qc.h(q_source[0])
qc.barrier()

# --- Step 4: Sender measures and sends classical info ---
# Alice measures her two qubits (the source and her entangled half).
qc.measure(q_source[0], c_classical[0])
qc.measure(q_entangled[0], c_classical[1])
qc.barrier()

# --- Step 5: Receiver's operations (controlled by classical info) ---
# The receiver (Bob) applies gates to his qubit based on the classical bits he received.
with qc.if_test((c_classical, 1)): # If the second classical bit is 1, apply X gate
    qc.x(q_entangled[1])
with qc.if_test((c_classical, 2)): # If the first classical bit is 1, apply Z gate
    qc.z(q_entangled[1])


# The state of Bob's qubit (q_entangled[1]) should now be identical to the
# initial random state of the source qubit.
# Note: We cannot measure Bob's qubit as that would collapse the state.
# Instead, simulators can show the final statevector.

print("Quantum Teleportation Circuit:")
print(qc.draw())

# --- Verification (using a simulator) ---
# We can use a statevector simulator to verify that the final state of Bob's qubit
# matches the initial state of the source qubit.
from qiskit.quantum_info import Statevector

# Simulate the circuit to get the final statevector
sv_sim = AerSimulator(method='statevector')
final_statevector = sv_sim.run(qc).result().get_statevector()

# The final state of Bob's qubit is in the last qubit's subspace.
# Because Qiskit's bit ordering is right-to-left, the last qubit is the first one.
# We need to extract this part of the statevector.
from qiskit.quantum_info import partial_trace
bob_final_state = partial_trace(final_statevector, [0, 1])

print("\n--- Verification ---")
print("Initial state of source qubit:\n", random_ket.data)
print("\nFinal state of Bob's qubit:\n", bob_final_state.data)

# Check if they are close (allowing for small floating point errors)
if np.allclose(random_ket.data, bob_final_state.data):
    print("\nSuccess! The state was teleported correctly.")
else:
    print("\nFailure. The states do not match.")
