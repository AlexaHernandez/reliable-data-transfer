#!/usr/bin/python2
import os,subprocess,sys

previous_dir = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.environ["GINI_ROOT"] = os.path.realpath("..")
os.environ["GINI_SHARE"] = os.path.realpath("../share/gini")
os.environ["GINI_LIB"] = os.path.realpath("../lib/gini")
os.environ["GINI_HOME"] = os.environ["HOME"] + "/.gini"
if not os.path.exists(os.environ["GINI_HOME"] + "/etc"): os.makedirs(os.environ["GINI_HOME"] + "/etc")
if not os.path.exists(os.environ["GINI_HOME"] + "/sav"): os.makedirs(os.environ["GINI_HOME"] + "/sav")
if not os.path.exists(os.environ["GINI_HOME"] + "/data"): os.makedirs(os.environ["GINI_HOME"] + "/data")
if not os.path.exists(os.environ["GINI_HOME"] + "/tmp"): os.makedirs(os.environ["GINI_HOME"] + "/tmp")
params = [os.path.realpath("../lib/gini/wgini/gwcenter.sh")]
if len(sys.argv) > 1: params.extend(sys.argv[1:])
os.chdir(previous_dir)
os.execv(params[0],params)
