from PiezoWebApp.src.utils.str_helper import is_str_empty
from PiezoWebApp.src.services.validator.validation_result import ValidationResult


def validate_name(value):
    if not isinstance(value, str):
        return ValidationResult(False, "name argument must be a string", None)
    if is_str_empty(value) is True:
        return ValidationResult(False, "name argument cannot be empty", None)
    return ValidationResult(True, None, value)


def validate_language(value):
    if not isinstance(value, str):
        return ValidationResult(False, "language argument must be a string", None)
    if str(value.lower()) not in ["python", "scala"]:
        return ValidationResult(False, "language must be either 'python' or 'Scala'", None)
    return ValidationResult(True, None, value)


def validate_python_version(value):
    string_value = str(value) if isinstance(value, int) else value
    if string_value not in ["2", "3"]:
            return ValidationResult(False, "Python version must be a string and either '2' or '3'", None)
    return ValidationResult(True, None, string_value)


def validate_path_to_main_app_file(value):
    if not isinstance(value, str):
        return ValidationResult(False, "path_to_main_app_file argument must be a string", None)
    if is_str_empty(value) is True:
        return ValidationResult(False, "path_to_main_app_file argument cannot be empty", None)
    return ValidationResult(True, None, value)


def validate_main_class(value):
    if not isinstance(value, str):
        return ValidationResult(False, "main_class argument must be a string", None)
    if is_str_empty(value) is True:
        return ValidationResult(False, "main_class argument cannot be empty", None)
    return ValidationResult(True, None, value)


def validate_driver_cores(value, min_value, max_value):
    if isinstance(value, int) or isinstance(value, float):
        is_valid = min_value <= value <= max_value if (value*10) % 1 == 0 else False
    elif isinstance(value, str):
        try:
            numerical_value = float(value[:-1])/1000 if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if (numerical_value*10) % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(False,
                                    "Driver cores must be of the form X (where X is an int or float and represents the"
                                    " number of cpus to the nearest 0.1 or 'Xm' (where Xm is a string and the m "
                                    "represents millicpus). Note: 0.1 == '100m', 1 == 1000m",
                                    None)
    else:
        is_valid = False
    return ValidationResult(True, None, value) if is_valid is True else ValidationResult(
        False,
        f"Driver core = {value} outside of valid range ({min_value}, {max_value}) or "
        f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'} and be given to 0.1 cpu (100m)",
        None)


def validate_driver_core_limit(value, min_value, max_value):
    if isinstance(value, int) or isinstance(value, float):
        is_valid = min_value <= value <= max_value if (value*10) % 1 == 0 else False
    elif isinstance(value, str):
        try:
            numerical_value = float(value[:-1])/1000 if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if (numerical_value*10) % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(False,
                                    "Driver core limit must be of the form X (where X is an int or float and represents"
                                    " the number of cpus to the nearest 0.1 or 'Xm' (where Xm is a string and the m "
                                    "represents millicpus). Note: 0.1 == '100m', 1 == 1000m",
                                    None)
    else:
        is_valid = False
    return ValidationResult(True, None, value) if is_valid is True else ValidationResult(
        False,
        f"Driver core limit = {value} outside of valid range ({min_value}, {max_value}) or "
        f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'} and be given to 0.1 cpu (100m)",
        None)


def validate_driver_memory(value, min_value, max_value):
    if isinstance(value, str):
        try:
            numerical_value = float(value[:-1]) if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(
                False,
                "Driver memory must be a string in the format 'Xm' where X is the number of megabytes,"
                "integers are also accepted but are assumed to also be megabytes.",
                None)
    elif isinstance(value, int) or isinstance(value, float):
        numerical_value = value
        is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
    else:
        return ValidationResult(False,
                                "Driver memory must be a string in the format 'Xm' where X is the number of megabytes,"
                                "integers are also accepted but are assumed to also be megabytes.",
                                None)
    if is_valid:
        return ValidationResult(True, None, numerical_value)
    return ValidationResult(False,
                            f"Driver memory = {value} is outside of valid range "
                            f"({str(min_value) + 'm'}, {str(max_value) + 'm'}", None)


def validate_executors(value, min_value, max_value):
    try:
        numerical_value = float(value)
    except ValueError:
        return ValidationResult(False, f"Executors argument must be an integer", None)
    is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
    if is_valid is True:
        return ValidationResult(True, None, value)
    return ValidationResult(
        False, f"Executors = {value} outside of valid values range ({min_value}, {max_value})", None)


def validate_executor_cores(value, min_value, max_value):
    if isinstance(value, int) or isinstance(value, float):
        is_valid = min_value <= value <= max_value if (value*10) % 1 == 0 else False
    elif isinstance(value, str):
        try:
            numerical_value = float(value[:-1])/1000 if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if (numerical_value*10) % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(False,
                                    "Executor cores must be of the form X (where X is an int or float and represents "
                                    "the number of cpus to the nearest 0.1 or 'Xm' (where Xm is a string and the m "
                                    "represents millicpus). Note: 0.1 == '100m', 1 == 1000m",
                                    None)
    else:
        is_valid = False
    return ValidationResult(True, None, value) if is_valid is True else ValidationResult(
        False,
        f"Executor core = {value} outside of valid range ({min_value}, {max_value}) or "
        f"({str(int(min_value*1000))+'m'}, {str(int(max_value*1000))+'m'} and be given to 0.1 cpu (100m)",
        None)


def validate_executor_memory(value, min_value, max_value):
    if isinstance(value, str):
        try:
            numerical_value = float(value[:-1]) if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(
                False,
                "Executor memory must be a string in the format 'Xm' where X is the number of megabytes,"
                "integers are also accepted but are assumed to also be megabytes.",
                None)
    elif isinstance(value, int) or isinstance(value, float):
        numerical_value = value
        is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
    else:
        return ValidationResult(False,
                                "Executor memory must be a string in the format 'Xm' where X is the number of megabytes"
                                ", integers are also accepted but are assumed to also be megabytes.",
                                None)
    if is_valid:
        return ValidationResult(True, None, numerical_value)
    return ValidationResult(False,
                            f"Executor memory = {value} is outside of valid range "
                            f"({str(min_value) + 'm'}, {str(max_value) + 'm'}", None)


def _validate_memory(value, min_value, max_value, format_error_msg, value_error_msg):
    if isinstance(value, str):
        try:
            numerical_value = float(value[:-1]) if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(
                False, format_error_msg, None)
    elif isinstance(value, int) or isinstance(value, float):
        numerical_value = value
        is_valid = min_value <= numerical_value <= max_value if numerical_value % 1 == 0 else False
    else:
        return ValidationResult(False, format_error_msg, None)
    if is_valid:
        return ValidationResult(True, None, numerical_value)
    return ValidationResult(False, value_error_msg, None)


def _validate_cores(value, min_value, max_value, format_error_msg, value_error_msg):
    if isinstance(value, int) or isinstance(value, float):
        is_valid = min_value <= value <= max_value if (value*10) % 1 == 0 else False
    elif isinstance(value, str):
        try:
            numerical_value = float(value[:-1])/1000 if value[-1] == "m" else float(value)
            is_valid = min_value <= numerical_value <= max_value if (numerical_value*10) % 1 == 0 else False
        except (ValueError, IndexError):
            return ValidationResult(False, format_error_msg, None)
    else:
        is_valid = False
    return ValidationResult(True, None, value) if is_valid is True else ValidationResult(
        False, value_error_msg, None)
