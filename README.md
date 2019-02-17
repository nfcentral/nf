NF is Not Framework
===================

Installation
------------

Just get [nf](https://github.com/iced/nf/blob/master/nf) and put it somewhere in $PATH. As nf dockers are not on dockerhub yet, you also need to build them locally - just clone and make, that's all.

Usage
-----

    nf new coolproj # creates new project with nf.json
    nf generate     # (re)generates everything you need
    nf build        # bulds your project
    nf freeze       # freeze python packages
    nf up           # starts all containers you need for development, app is epxosed to :8000

To edit your code you need any editor from the list of editors which can properly edit projects over ssh. As this list starts and ends with emacs, just point your emacs to `ssh://root@localhost#2222:/app` and you are good to go. If you need completions and code introspection - standard [anaconda-mode](https://github.com/proofit404/anaconda-mode) setup should work.

Features
--------

You can enable set of features for your project. Each feature can have set of subfeatures, in this case you can just use `feature[subfeature1,subfeature2]`.

    jupyter         # creates jupyter container with access to your app code exposed to :8888
        plots       # adds matplotlib and seaborn (trust me, you don't want to deal with this yourself)
    postgres        # postgres support, only libs at the moment, more to come

System Dependencies
-------------------

You can also add system dependencies needed either for your app or for python libs you are uisng.

    dependencies            # dependencies needed at runtime for all images
    dependencies_build      # dependencies needed only at build time for all images
    dependencies_dev        # dependencies needed at runtime for dev images
    dependencies_dev_build  # dependencies needed only at build time for all images
