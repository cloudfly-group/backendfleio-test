from typing import Dict
from typing import Optional

from django.conf import settings
from typing import List


class Features(object):
    def __init__(self, features: Dict[str, bool], dependencies: Optional[Dict[str, List[str]]] = None):
        features['core'] = True  # core feature is always true
        self.all = features
        self.parent_feature_names = []
        for name in self.all:
            parent_feature_name = Features.get_parent_feature_name(name)
            if parent_feature_name in self.all and parent_feature_name not in self.parent_feature_names:
                self.parent_feature_names.append(parent_feature_name)

        new_parent_feature_names = []

        for feature_name in self.all:
            parent_feature_name = Features.get_parent_feature_name(feature_name)

            if parent_feature_name:
                if parent_feature_name not in self.parent_feature_names:
                    # set main feature enabled if not found
                    if parent_feature_name not in new_parent_feature_names:
                        new_parent_feature_names.append(parent_feature_name)
                else:
                    # set feature disabled if main feature is disabled
                    if not self.all.get(parent_feature_name, False):
                        self.all[feature_name] = False

        self.parent_feature_names += new_parent_feature_names

        for parent_feature_name in new_parent_feature_names:
            self.all[parent_feature_name] = True

        if dependencies:
            for feature_name in dependencies:
                if feature_name in self.all:
                    for needed_feature_name in dependencies[feature_name]:
                        needed_feature_enabled = self.all.get(needed_feature_name, False)
                        self.all[feature_name] = self.all[feature_name] and needed_feature_enabled

    @staticmethod
    def get_parent_feature_name(feature_name: str) -> Optional[str]:
        if '.' in feature_name:
            split_position = feature_name.rfind('.')
            parent_feature_name = feature_name[:split_position]
            return parent_feature_name
        else:
            return None

    def is_enabled(self, feature_name: str) -> bool:
        return self.all.get(feature_name, False)

    def has_feature(self, feature_name: str) -> bool:
        return feature_name in self.all.keys()

    def get_disabled_features(self) -> list:
        disabled_features = list()
        for feature_name, value in self.all.items():
            if value is False:
                disabled_features.append(feature_name)
        return disabled_features

    def is_at_least_one_feature_enabled(self, feature_list: List[str]) -> bool:
        enabled = False  # type: bool
        for feature_name in feature_list:
            enabled = enabled or self.is_enabled(feature_name=feature_name)

        return enabled


active_features = Features(settings.FEATURES, settings.FEATURES_DEPENDENCIES)
staff_active_features = Features(settings.STAFF_FEATURES, settings.STAFF_FEATURES_DEPENDENCIES)
reseller_active_features = Features(settings.RESELLER_FEATURES, settings.RESELLER_FEATURES_DEPENDENCIES)
