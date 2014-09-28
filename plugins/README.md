Plugins
===

All plugins must live in their own folder, with at least the following:

```
plugin_name/
  - plugin.yml
  - __init__.py
```

The `plugin.yml` should look like this:

```yaml
name: Plugin Name
description: Plugin description
version: 1.0
author: Plugin Author
requires:
  - item1
  - item2
soft-requires:
  - item4
provides:
  - item16
autoload: true
disabled: false
```

The only required item is `name`.  If there are other types of plugins that you depend on, the specific provider type you are looking for should be in `requires`.  If you plugin supports multiple things, and some are not completely required for your plugin to function then you can list them in `soft-requires`.  If you plugin provides something specifically for other plugins to use, then you should list what it provides in the `provides`.  `autoload` is whether your plugin should be automatically loaded at start.  If you plugin is simply a provider, this should be `false` as it there is another plugin that requires it, it will automatically be loaded anyway.  If you specify a plugin as `disabled` it will not run at all.
