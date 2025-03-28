# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright 2025 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""EstimatorV2 example with IBM Direct Access QRMI"""

# pylint: disable=invalid-name
import os
import json
from dotenv import load_dotenv
from qiskit.circuit.library import QAOAAnsatz
from qiskit.transpiler import generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime.utils.backend_converter import convert_to_target
from qiskit_ibm_runtime.models import BackendProperties, BackendConfiguration
from qrmi_primitives.ibm import IBMDirectAccessEstimatorV2
from qrmi import IBMDirectAccess

load_dotenv()

qrmi = IBMDirectAccess()
target = qrmi.target(os.environ["QRMI_RESOURCE_ID"])
target = json.loads(target.value)
backend_config = BackendConfiguration.from_dict(target["configuration"])
print(backend_config)
backend_props = BackendProperties.from_dict(target["properties"])
print(backend_props)

# Generate transpiler target from backend configuration & properties
target = convert_to_target(backend_config, backend_props)

entanglement = [tuple(edge) for edge in target.build_coupling_map().get_edges()]
observable = SparsePauliOp.from_sparse_list(
    [("ZZ", [i, j], 0.5) for i, j in entanglement],
    num_qubits=target.num_qubits,
)
circuit = QAOAAnsatz(observable, reps=2)
# the circuit is parametrized, so we will define the parameter values for execution
param_values = [0.1, 0.2, 0.3, 0.4]

print(f">>> Observable: {observable.paulis}")

pm = generate_preset_pass_manager(
    optimization_level=1,
    target=target,
)
isa_circuit = pm.run(circuit)
isa_observable = observable.apply_layout(isa_circuit.layout)
print(f">>> Circuit ops (ISA): {isa_circuit.count_ops()}")

estimator = IBMDirectAccessEstimatorV2()

job = estimator.run([(isa_circuit, isa_observable, param_values)])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")

result = job.result()
print(f">>> {result}")
print(f"  > Expectation value: {result[0].data.evs}")
print(f"  > Metadata: {result[0].metadata}")
