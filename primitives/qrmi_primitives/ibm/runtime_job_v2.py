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

"""Runtime job"""

import time
from qiskit_ibm_runtime.utils.result_decoder import ResultDecoder
from qiskit.primitives import BasePrimitiveJob, PrimitiveResult
from qrmi import IBMDirectAccess, TaskStatus


class RuntimeJobV2(BasePrimitiveJob[PrimitiveResult, TaskStatus]):
    """Representation of a runtime V2 primitive exeuction.
    """

    def __init__(
        self,
        qrmi: IBMDirectAccess,
        job_id: str,
        *,
        delete_job: bool = False
    ) -> None:
        """RuntimeJob constructor.

        Args:
            qrmi: QRMI object for IBM Direct Access.
            job_id: Job ID.
            delete_job: True if you want delete Direct Access job in the destructor.
        """
        self._qrmi = qrmi
        self._job_id = job_id
        self._last_status = None
        self._result = None
        self._delete_job = delete_job

    def __del__(self):
        """RuntimeJob destructor.
        """
        if self._delete_job is True:
            self._qrmi.task_stop(self._job_id)

    def job_id(self) -> str:
        """Return a unique id identifying the job.
        """
        return self._job_id

    def cancel(self) -> None:
        """Cancel the job.
        """
        self._qrmi.task_stop(self._job_id)

    def result(self) -> PrimitiveResult:
        """Return the results of the job.
        """
        if self._last_status is not None and self._result is not None:
            return self._result

        while True:
            if self.in_final_state() is True:
                break

            time.sleep(1)

        result = self._qrmi.task_result(self._job_id)
        self._result = ResultDecoder.decode(result.value)
        return self._result

    def status(self) -> TaskStatus:
        """Return the status of the job.

        Returns:
            Status of this job.
        """
        if self._last_status is None or self._last_status in [
            TaskStatus.Queued,
            TaskStatus.Running,
        ]:
            self._last_status = self._qrmi.task_status(self._job_id)
        return self._last_status

    def done(self) -> bool:
        """Return whether the job has successfully run.
        """
        return self.status() == TaskStatus.Completed

    def running(self) -> bool:
        """Return whether the job is actively running.
        """
        return self.status() == TaskStatus.Running

    def cancelled(self) -> bool:
        """Return whether the job has been cancelled.
        """
        return self.status() == TaskStatus.Cancelled

    def in_final_state(self) -> bool:
        """Return whether the job is in a final job state such as ``DONE`` or ``ERROR``.
        """
        return self.status() in [
            TaskStatus.Completed,
            TaskStatus.Cancelled,
            TaskStatus.Failed,
        ]
