from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler


# pylint: disable=abstract-method
class GetJobsHandler(BaseHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "spark_jobs": {
                    "type": "object",
                    "properties": {
                        "job_name": {"type": "string"},
                        "status": {"type": "string"}
                    }
                }
            },
        }
    )
    def get(self, *args, **kwargs):
        result = self._spark_job_service.get_jobs()
        self._logger.debug(f'Getting list of spark applications present returned: "{result["status"]}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
