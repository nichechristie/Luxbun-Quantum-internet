#!/usr/bin/env python3
"""
Submit a real quantum job to IBM Quantum for verification
"""

import os
import sys
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_provider import IBMProvider

def main():
    # Set token
    token = os.environ.get('QISKIT_IBM_TOKEN') or os.environ.get('IBM_TOKEN')
    if not token:
        print("❌ No IBM token found. Set QISKIT_IBM_TOKEN or IBM_TOKEN environment variable")
        return

    print("🚀 Connecting to IBM Quantum...")

    try:
        # Use the instance CRN for potential premium access
        instance_crn = 'crn:v1:bluemix:public:quantum-computing:us-east:a/4c416b81be5443be9329086c6afcdece:19ca0932-7a35-4c98-a032-370414c6840c::'
        provider = IBMProvider(token=token, instance=instance_crn)
        print("✅ Connected to IBM Quantum with instance!")

        # Get available backends
        backends = provider.backends()
        real_backends = [b for b in backends if not b.simulator and b.status().operational]
        print(f"✅ Found {len(real_backends)} operational quantum computers")

        if not real_backends:
            print("❌ No operational quantum computers available")
            return

        # Use the first available backend
        backend = real_backends[0]
        print(f"🎯 Using backend: {backend.name} ({backend.num_qubits} qubits)")

        # Create a simple quantum circuit (1 qubit, 1 measurement)
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Hadamard gate for superposition
        qc.measure(0, 0)

        print("⚛️ Created quantum circuit: Hadamard + Measure")
        print("📊 Circuit will generate true quantum randomness")

        # Transpile for the backend
        transpiled_qc = transpile(qc, backend)

        # Submit job using backend.run (legacy API, works with free tier)
        print(f"📡 Submitting job to {backend.name}...")
        job = backend.run(transpiled_qc, shots=1024)

        job_id = job.job_id()
        print("🎉 REAL QUANTUM JOB SUBMITTED SUCCESSFULLY!")
        print(f"📋 Job ID: {job_id}")
        print(f"🔗 Track job status: https://quantum.ibm.com/jobs/{job_id}")
        print("⏳ Job submitted - check dashboard for completion")
        print("💡 This should appear on your IBM Quantum dashboard!")

    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()