import unittest
import pytest

from PiezoWebApp.src.config.spark_job_validation_rules import LANGUAGE_SPECIFIC_KEYS
from PiezoWebApp.src.config.spark_job_validation_rules import VALIDATION_RULES
from PiezoWebApp.src.services.spark_job.validation.manifest_populator import ManifestPopulator
from PiezoWebApp.src.services.spark_job.validation.validation_ruleset import ValidationRuleset


class TestTemplatePopulator(unittest.TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        validation_ruleset = ValidationRuleset(LANGUAGE_SPECIFIC_KEYS, VALIDATION_RULES)
        self.test_populator = ManifestPopulator(validation_ruleset)
        self.arguments = {"name": "test",
                          "path_to_main_app_file": "/path/to/file",
                          "driver_cores": 0.1,
                          "driver_core_limit": "200m",
                          "driver_memory": "512m",
                          "executor_cores": 1,
                          "executors": 1,
                          "executor_memory": "512m"}

    def test_build_manifest_builds_python_job_manifest_for_python_applications(self):
        # Arrange
        self.arguments["language"] = "Python"
        self.arguments["python_version"] = "2"
        # Act
        manifest = self.test_populator.build_manifest(self.arguments)
        # Assert
        self.assertDictEqual(manifest, {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                                        "kind": "SparkApplication",
                                        "metadata":
                                            {"name": "test",
                                             "namespace": "default"},
                                        "spec": {
                                            "type": "Python",
                                            "pythonVersion": "2",
                                            "mode": "cluster",
                                            "image": "gcr.io/spark-operator/spark:v2.4.0",
                                            "imagePullPolicy": "Always",
                                            "mainApplicationFile": "/path/to/file",
                                            "sparkVersion": "2.4.0",
                                            "restartPolicy": {
                                                "type": "Never"},
                                            "driver": {
                                                "cores": 0.1,
                                                "coreLimit": "200m",
                                                "memory": "512m",
                                                "labels": {
                                                    "version": "2.4.0"},
                                                "serviceAccount": "spark"},
                                            "executor": {
                                                "cores": 1,
                                                "instances": 1,
                                                "memory": "512m",
                                                "labels": {
                                                    "version": "2.4.0"}}}})

    def test_build_manifest_builds_scala_job_manifest_for_scala_applications(self):
        # Arrange
        self.arguments["language"] = "Scala"
        self.arguments["main_class"] = "testClass"
        # Act
        manifest = self.test_populator.build_manifest(self.arguments)
        # Assert
        self.assertDictEqual(manifest, {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                                        "kind": "SparkApplication",
                                        "metadata":
                                            {"name": "test",
                                             "namespace": "default"},
                                        "spec": {
                                            "type": "Scala",
                                            "mode": "cluster",
                                            "image": "gcr.io/spark-operator/spark:v2.4.0",
                                            "imagePullPolicy": "Always",
                                            "mainApplicationFile": "/path/to/file",
                                            "mainClass": "testClass",
                                            "sparkVersion": "2.4.0",
                                            "restartPolicy": {
                                                "type": "Never"},
                                            "driver": {
                                                "cores": 0.1,
                                                "coreLimit": "200m",
                                                "memory": "512m",
                                                "labels": {
                                                    "version": "2.4.0"},
                                                "serviceAccount": "spark"},
                                            "executor": {
                                                "cores": 1,
                                                "instances": 1,
                                                "memory": "512m",
                                                "labels": {
                                                    "version": "2.4.0"}}}})

    def test_default_manifest_returns_a_filled_in_spark_application_template_with_default_values(self):
        # Arrange
        default_manifest = self.test_populator._default_spark_application_manifest()
        # Assert
        self.assertDictEqual(default_manifest, {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                                                "kind": "SparkApplication",
                                                "metadata":
                                                    {"name": None,
                                                     "namespace": "default"},
                                                "spec": {
                                                    "mode": "cluster",
                                                    "image": "gcr.io/spark-operator/spark:v2.4.0",
                                                    "imagePullPolicy": "Always",
                                                    "mainApplicationFile": None,
                                                    "sparkVersion": "2.4.0",
                                                    "restartPolicy": {
                                                        "type": "Never"},
                                                    "driver": {
                                                        "cores": 0.1,
                                                        "coreLimit": 0.2,
                                                        "memory": "512m",
                                                        "labels": {
                                                            "version": "2.4.0"},
                                                        "serviceAccount": "spark"},
                                                    "executor": {
                                                        "cores": 1,
                                                        "instances": 1,
                                                        "memory": "512m",
                                                        "labels": {
                                                            "version": "2.4.0"}}}})