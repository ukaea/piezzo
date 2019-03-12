from abc import ABCMeta, abstractmethod


class IKubernetesAdapter(metaclass=ABCMeta):

    # pylint: disable=too-many-arguments
    @abstractmethod
    def delete_namespaced_custom_object(self, group, version, namespace, plural, name, body):
        pass

    # pylint: disable=too-many-arguments
    @abstractmethod
    def delete_options(self,
                       api_version=None,
                       dry_run=None,
                       grace_period_seconds=None,
                       kind=None,
                       orphan_dependents=None,
                       pre_conditions=None,
                       propagation_policy=None):
        pass

    @abstractmethod
    def read_namespaced_pod_log(self, driver_name, namespace):
        pass

    # pylint: disable=too-many-arguments
    @abstractmethod
    def create_namespaced_custom_object(self, group, version, namespace, plural, body):
        pass

    @abstractmethod
    def get_namespaced_custom_object(self, group, version, namespace, plural, name):
        pass

    @abstractmethod
    def list_namespaced_custom_object(self, group, version, namespace, plural):
        pass
