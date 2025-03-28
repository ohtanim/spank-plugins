# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright 2024, 2025 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""SamplerV2 example with IBM Direct Access QRMI"""

# pylint: disable=invalid-name
import os
import json
import numpy as np
from dotenv import load_dotenv
from qiskit.circuit.library import EfficientSU2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.utils.backend_converter import convert_to_target
from qiskit_ibm_runtime.models import BackendProperties, BackendConfiguration
from qrmi_primitives.ibm import IBMDirectAccessSamplerV2
from qrmi import IBMDirectAccess

load_dotenv()

qrmi = IBMDirectAccess()
target = qrmi.target(os.environ["QRMI_RESOURCE_ID"])
target = json.loads(target.value)
backend_config = BackendConfiguration.from_dict(target["configuration"])
print(backend_config)
backend_props = BackendProperties.from_dict(target["properties"])
print(backend_props)

circuit = EfficientSU2(127, entanglement="linear", flatten=True)
circuit.measure_all()
# The circuit is parametrized, so we will define the parameter values for execution
param_values = np.random.rand(circuit.num_parameters)

# Generate transpiler target from backend configuration & properties
target = convert_to_target(backend_config, backend_props)
pm = generate_preset_pass_manager(
    optimization_level=1,
    target=target,
)
isa_circuit = pm.run(circuit)
print(f">>> Circuit ops (ISA): {isa_circuit.count_ops()}")

sampler = IBMDirectAccessSamplerV2()
job = sampler.run([(isa_circuit, param_values)])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")
result = job.result()

# Get results for the first (and only) PUB
pub_result = result[0]
print(f"Counts for the 'meas' output register: {pub_result.data.meas.get_counts()}")
