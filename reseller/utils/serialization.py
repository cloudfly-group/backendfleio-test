from fleio.reseller.utils import user_reseller_resources


class CurrentResellerResourcesDefault:
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user
        self.reseller_resources = user_reseller_resources(user=self.user)

    def __call__(self):
        return self.reseller_resources

    def __repr__(self):
        return '%s()' % self.__class__.__name__
