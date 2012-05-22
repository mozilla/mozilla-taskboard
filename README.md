Install
-------

Clone it
$ vagrant up
$ vagrant ssh

Now in the VM:
$ cd mozilla-taskboard/
$ sudo pip install -f ./requirements/dev.txt
$ python ./manage syncdb
$ python ./manage runserver 0.0.0.0:8000

License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/

