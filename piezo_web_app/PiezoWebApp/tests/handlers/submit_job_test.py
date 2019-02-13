from tornado.testing import gen_test

from PiezoWebApp.tests.handlers.base_handler_test import BaseHandlerTest
from PiezoWebApp.src.handlers.submit_job import SubmitJobHandler


class SubmitJobHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return SubmitJobHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @gen_test
    def test_post_returns_400_when_job_name_is_missing(self):
        body = {'namespace': 'example-namespace'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_post_returns_400_when_namespace_is_missing(self):
        body = {'job_name': 'example-spark-job'}
        yield self.assert_request_returns_400(body)

    @gen_test
    def test_post_returns_confirmation_of_submit_when_successful(self):
        # Arrange
        body = {'job_name': 'test-spark-job', 'namespace': 'test-namespace'}
        self.mock_kubernetes_adapter.submit_job.return_value = '{"message": "job test-spark-job submitted success"}'
        # Act
        response_body, response_code = yield self.send_request(body)
        # Assert
        self.mock_kubernetes_adapter.submit_job.assert_called_once_with(body)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == '{"message": "job test-spark-job submitted success"}'
