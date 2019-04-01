import json
import pytest
from tornado.httpclient import HTTPError
from tornado.testing import gen_test
from kubernetes.client.rest import ApiException

from PiezoWebApp.src.handlers.delete_job import DeleteJobHandler
from PiezoWebApp.tests.integration_tests.base_integration_test import BaseIntegrationTest

# str | The custom resource's group name
CRD_GROUP = 'sparkoperator.k8s.io'

# str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
CRD_PLURAL = 'sparkapplications'

# str | The custom resource's version
CRD_VERSION = 'v1beta1'

NAMESPACE = 'default'


class DeleteJobIntegrationTest(BaseIntegrationTest):
    @property
    def handler(self):
        return DeleteJobHandler

    @property
    def standard_request_method(self):
        return 'DELETE'

    @gen_test
    def test_success_message_is_returned_when_job_deleted_successfully(self):
        # Arrange
        body = {"job_name": "test-spark-job"}
        kubernetes_response = {'status': 'Success'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.return_value = kubernetes_response
        self.mock_k8s_adapter.delete_options.return_value = {"api_version": "version", "other_values": "values"}
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        assert self.mock_k8s_adapter.delete_namespaced_custom_object.call_count == 1
        self.mock_k8s_adapter.delete_namespaced_custom_object.assert_called_once_with(CRD_GROUP,
                                                                                      CRD_VERSION,
                                                                                      NAMESPACE,
                                                                                      CRD_PLURAL,
                                                                                      'test-spark-job',
                                                                                      {
                                                                                          "api_version": "version",
                                                                                          "other_values": "values"
                                                                                      })
        assert response_code == 200
        self.assertDictEqual(response_body, {
            'status': 'success',
            'data': {
                'message': '"test-spark-job" deleted'
            }
        })

    @gen_test
    def test_trying_to_delete_non_existent_job_returns_404_with_reason(self):
        # Arrange
        body = {'job_name': 'test-spark-job'}
        self.mock_k8s_adapter.delete_namespaced_custom_object.side_effect = ApiException(status=404, reason="Not Found")
        # Act
        with pytest.raises(HTTPError) as exception:
            yield self.send_request(body)
        assert exception.value.response.code == 404
        msg = json.loads(exception.value.response.body, encoding='utf-8')['data']
        assert msg == 'Kubernetes error when trying to delete job "test-spark-job": Not Found'
