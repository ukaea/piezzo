import uuid

from kubernetes.client.rest import ApiException

from PiezoWebApp.src.services.spark_job.i_spark_job_namer import ISparkJobNamer
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION


class SparkJobNamer(ISparkJobNamer):
    def __init__(self, kubernetes_adapter, validation_ruleset):
        self._namespace = validation_ruleset.get_default_value_for_key("namespace")
        self._kubernetes_adapter = kubernetes_adapter
        self._max_attempts = 10

    def rename_job(self, base_name):
        counter = 0
        while counter < self._max_attempts:
            trial_job_name = self._tag_job_name_with_uuid(base_name)
            counter += 1
            if not self._does_job_exist(trial_job_name):
                break
        if counter >= self._max_attempts:
            raise RuntimeError(f'{counter} attempts to find a unique job name all failed')
        return trial_job_name

    def _does_job_exist(self, job_name):
        try:
            self._kubernetes_adapter.get_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                self._namespace,
                CRD_PLURAL,
                job_name
            )
            return True
        except ApiException:
            return False

    @staticmethod
    def _tag_job_name_with_uuid(base_name):
        # UUIDs are sequences of 32 hexadecimal digits separated by hyphens
        # 32 hexadecimal digits have a total number of possible combinations that is over 3.4E38
        # Here we trim the UUID to just 8 hexadecimal digits
        # 16 hexadecimal digits have a total number of possible combinations that is over 4.2E9
        uuid_tag = str(uuid.uuid4())[:8]
        return f'{base_name}-{uuid_tag}'