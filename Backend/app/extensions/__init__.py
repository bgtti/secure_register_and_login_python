"""
**The extensions package**

Contains the files necessary to configure extensions to the flask functionality.

--------------------------------------
It is useful to keep the initiation of extensions in one file, so that an overview of what is being used can be obtain at a glance. This is the reason `extensions.py` was created. 

The extensions are not only listed in `extensions.py`, but the packages are imported into other files from it. It is intended as the central source of truth for external packages.

Necessary extension-specific configuration should also be included in this directory (**extensions package**). An example of this is `login_manager_config.py`, which contains functions necessary for the Flask-Login manager extension to work.

"""