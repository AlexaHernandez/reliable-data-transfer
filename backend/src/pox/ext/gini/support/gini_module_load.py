#!/usr/bin/python2

"""
gini_module_load.py

Watches a particular file for the addition of new module names. The modules
with those names are imported into POX and executed. This allows modules
to be loaded from gBuilder.
"""

from pox.core import core
import pox.lib.util as poxutil
import pox.openflow.libopenflow_01 as of
import os, time, threading, importlib

log = core.getLogger()

class ModuleFileReader(threading.Thread):
    def __init__(self, module_file_path):
        threading.Thread.__init__(self)
        self.module_file_path = module_file_path
        # self.launched_modules = []
        self.current_module = None

    def run(self):
        """
        Rewritten by Trung

        The current implementation of run() is supposed to load only one Gini
        module at a time. To load a new module, the current one must be unloaded
        and cleaned from the core object.

        To unload the current module, all the rules stored in core.openflow will
        be flushed, and all connected switches should also reset their flow tables

        If the module has registered a new component in core object, then that
        component could be deleted as well, although this step may require some
        addition to the third-party code.
        """
        while True:
            time.sleep(5)

            try:
                module_file = open(self.module_file_path, "r")
                module = module_file.readline().strip()

                if module == "":
                    pass
                elif self.current_module and module == self.current_module.__name__:
                    pass
                else:
                    if self.current_module is not None:
                        log.info("Remove current handlers and flows..")
                        core.openflow._eventMixin_handlers.clear()

                        msg = of.ofp_flow_mod(match=of.ofp_match(), command=of.OFPFC_DELETE)
                        for connection in core.openflow._connections.values():
                            connection.send(msg)
                        del self.current_module
                    log.info("gini_module_load: loading module - " + module)
                    try:
                        mod = importlib.import_module(module)
                        try:
                            mod.launch()
                            self.current_module = mod
                        except Exception as e:
                            log.error("gini_module_load: failed to launch module - " + module)
                    except Exception as e:
                        log.error("gini_module_load: module does not exist - " + module)

                """
                modules = module_file.readlines()
                for module in modules:
                    module = module.strip()
                    if module != "" and not module in self.launched_modules:
                        log.info(str(self.launched_modules))
                        log.info("gini_module_load: loading module - " + module)
                        try:
                            mod = importlib.import_module(module)
                            try:
                                mod.launch()
                            except Exception as e:
                                log.error("gini_module_load: failed to launch module - " + module)
                        except Exception as e:
                            log.error("gini_module_load: module does not exist - " + module)

                        self.launched_modules.append(module)
                        log.info(str(self.launched_modules))
                """

                module_file.close()
            except Exception as e:
                pass

@poxutil.eval_args
def launch(module_file_path):
    module_file_reader = ModuleFileReader(module_file_path)
    module_file_reader.start()
