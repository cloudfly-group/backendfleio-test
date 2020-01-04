
def gateway_action(methods=None, **kwargs):
    """Used to mark a method on a gateway module."""
    methods = ['get'] if (methods is None) else methods

    def decorator(func):
        func.allowed_methods = [m.lower() for m in methods]
        func.action = True
        func.kwargs = kwargs
        return func
    return decorator


def staff_gateway_action(display_name='', methods=None, transaction_statuses=None, requires_redirect=False, **kwargs):
    """Used to mark a method on a gateway module."""
    methods = ['get'] if (methods is None) else methods
    transaction_statuses = [] if (transaction_statuses is None) else transaction_statuses

    def decorator(func):
        func.display_name = display_name or func.__name__.title().replace('_', ' ')
        func.allowed_methods = [m.lower() for m in methods]
        func.staff_action = True
        func.transaction_statuses = transaction_statuses
        func.requires_redirect = requires_redirect
        func.kwargs = kwargs
        return func
    return decorator
