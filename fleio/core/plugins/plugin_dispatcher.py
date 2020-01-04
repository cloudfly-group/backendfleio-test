from logging import getLogger
from typing import Callable
from typing import List
from typing import Optional

from django.dispatch import Signal


LOG = getLogger(__name__)
ABORT_ON_BAD_ARGS = True


class PluginDispatcher(object):
    signals = {}
    functions = {}

    def register_signal(self, plugin: str, signal_name: str, signal: Signal):
        plugin_signals = self.signals.setdefault(plugin, {})
        if signal_name in plugin_signals:
            LOG.error('Signal {} already registered for plugin {}'.format(signal_name, plugin))
        else:
            plugin_signals[signal_name] = signal

    def register_function(self, plugin: str, function_name: str, func: Callable, required_args: Optional[List]):
        plugin_functions = self.functions.setdefault(plugin, {})
        if function_name in plugin_functions:
            LOG.error('Function {} already registered for plugin {}'.format(function_name, plugin))
        else:
            plugin_functions[function_name] = {
                'function': func,
                'required_args': required_args if required_args else []
            }

    def call_function(self, plugin: str, function_name: str, **kwargs):
        plugin_functions = self.functions.get(plugin, None)
        called = False
        if plugin_functions:
            func = plugin_functions.get(function_name, None)
            if func:
                # validate arguments
                for arg in func['required_args']:  # type: str
                    if arg not in kwargs:
                        LOG.error('Function {} for plugin {} needs argument {}'.format(function_name, plugin, arg))
                        if ABORT_ON_BAD_ARGS:
                            raise ValueError(
                                'Function {} for plugin {} needs argument {}'.format(function_name, plugin, arg)
                            )

                func['function'](**kwargs)
                called = True

        if not called:
            LOG.debug('Function {} for plugin {} was not found.'.format(function_name, plugin))

    def connect_to_signal(self, plugin: str, signal_name: str, receiver: Callable, dispatch_uuid: str = None):
        plugin_signals_dict = self.signals.get(plugin, None)
        connected = False
        if plugin_signals_dict:
            signal = plugin_signals_dict.get(signal_name, None)  # type: Signal
            if signal:
                signal.connect(
                    receiver=receiver,
                    dispatch_uid=dispatch_uuid,
                )
                connected = True

        if not connected:
            LOG.debug('Signal {} for plugin {} was not found'.format(signal_name, plugin))


plugin_dispatcher = PluginDispatcher()
