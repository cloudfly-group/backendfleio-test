from rest_framework import routers


class SharedRouter(routers.SimpleRouter):
    """Used to unify all URL's in a single DefaultRouter."""

    shared_router = routers.DefaultRouter(trailing_slash=False)

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)
        super(SharedRouter, self).register(*args, **kwargs)
