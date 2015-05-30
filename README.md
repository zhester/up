up
==

Upstanding Server Management Support Tools

Status
------

This is an in-development project to provide some much-needed automation
across my many home and work servers.

Features
--------

### Periodic File Backups

Called periodically to run `rsync` across a set of configured directories.

### Periodic Status/Situation Updates

Called periodically to report on various pieces of system status.  It's a
massively simplified, poor-man's SNMP-like tool.

Interface
---------

The planned interface is to install a system-wide script named `up`.  This
would be a Python script with sub-commands.  The initial sub-commands are
`back` (backup) and `sit` (situation update).  I'd like to also invent a
reason to make other tools called "build up," "pick up," and "mess up."

