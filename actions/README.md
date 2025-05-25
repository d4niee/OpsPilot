Neue Projekt-Typen: Einfach unter docker_configs einen neuen Key (z.B. "node-api") anlegen, mit eigenen basic/multi-stage Templates und passenden defaults.

Templates: In deinem templates/-Ordner die .j2-Dateien entsprechend ablegen, und in den Defaults die nötigen Parameter (z.B. build_tool, jar_dest) setzen.

Extensibilität: Sollten später weitere Parameter nötig sein (z.B. ENV-Vars, Labels), ergänze sie einfach im defaults-Dict und im Template.