def validate_client_limit():
    try:
        from fleio.core.loginview import validate_client_limit_impl
        return validate_client_limit_impl()
    except (ImportError, Exception):
        return True


def validate_services_limit():
    try:
        from fleio.core.loginview import validate_services_limit_impl
        return validate_services_limit_impl()
    except (ImportError, Exception):
        return True


def validate_cloud_objects_limit():
    try:
        from fleio.core.loginview import validate_cloud_objects_limit_impl
        return validate_cloud_objects_limit_impl()
    except (ImportError, Exception):
        return True
