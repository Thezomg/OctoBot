from os import listdir
import os.path
import yaml

import importlib

import logging
logger = logging.getLogger('octobot:PluginManager')

class Plugin(object):

    def __init__(self, loader, path):
        self.loader = loader
        self.module = None
        self.loaded = False
        self.path = path

        f = open(os.path.join(path, 'plugin.yml'))
        contents = yaml.load(f)

        self.name = contents['name'] if 'name' in contents else None
        if self.name is None:
            raise PluginException('Plugin name is required')

        self.requires = contents['requires'] if 'requires' in contents else []
        self.soft_requires = contents['soft-requires'] if 'soft-requires' in contents else []
        self.provides = contents['provides'] if 'provides' in contents else []
        self.description = contents['description'] if 'description' in contents else None
        self.version = contents['version'] if 'version' in contents else None
        self.author = contents['author'] if 'author' in contents else "unknown author"
        self.autoload = contents['autoload'] if 'autoload' in contents else False
        self.disabled = contents['disabled'] if 'disabled' in contents else False

        self.should_load = False

    def load(self):
        try:
            logger.info("Loading plugin {} by {}".format(self.name, self.author))
            if self.loaded == True and self.module:
                logger.info("Module already loaded, unregistering events")
                EventManager.unregisterModuleFunctions(self.module)
            self.module = self.loader.load_module()
            self.loaded = True
            return True
        except ImportError:
            logger.error("Failed to load module {} from {}".format(self.name, self.path))
            return False

class PluginManager(object):
    def __init__(self, paths):
        self.plugin_paths = paths
        self.plugins = []
        self.providers = {}

    def load_plugins(self):
        items = []
        for path in self.plugin_paths:
            for i in listdir(path):
                p = os.path.join(path, i)
                if os.path.isdir(p):
                    items.append(p)

        for i in items:
            p = os.path.join(i, 'plugin.yml')
            if os.path.exists(p):
                logger.debug("loading {} from {}".format(os.path.basename(i), os.path.dirname(i)))
                loader = importlib.find_loader('{}'.format(os.path.basename(i)), [os.path.dirname(i)])

                try:
                    plugin = Plugin(loader, i)
                    if plugin.disabled:
                        continue
                except PluginException as exc:
                    logger.error("Failed to load plugin: {}".format(str(exc)))
                    continue

                for i in plugin.provides:
                    if not i in self.providers:
                        self.providers[i] = []
                    self.providers[i].append(plugin)

                logger.info("Checking if plugins required")

                if plugin.autoload and self.haveRequired(plugin):
                    self.enableRequired(plugin)
                    self.set_to_load(plugin, additional="set to autoload in configuration")

                self.plugins.append(plugin)

        for p in self.plugins:
            if p.should_load:
                p.load()

    def set_to_load(self, *plugins, additional=None):
        for plugin in plugins:
            if not plugin.should_load:
                if additional is not None:
                    logger.debug("Setting {} by {} to load, {}".format(plugin.name, plugin.author, additional))
                else:
                    logger.debug("Setting {} by {} to load".format(plugin.name, plugin.author))
                plugin.should_load = True
                if self.haveRequired(plugin):
                    self.enableRequired(plugin)

    def registerProvider(self, provides, provider):
        if provider.lower() in self.providers:
            raise RegistrationException
        else:
            self.providers[provides.lower()] = provider

    def haveRequired(self, plugin):
        for i in plugin.requires:
            if not i.lower() in self.providers:
                logger.info("There are no providers for {} as requested by {}".format(i, plugin.name))
                return False

        return True

    def enableRequired(self, plugin):
        for i in plugin.requires + plugin.soft_requires:
            if i.lower() in self.providers:
                self.set_to_load(*self.providers[i.lower()], additional="required for {} by {}".format(i, plugin.name))