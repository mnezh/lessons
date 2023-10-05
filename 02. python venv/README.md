# venv — Creation of virtual python environments

The [venv](https://docs.python.org/3/library/venv.html) module supports creating lightweight “virtual environments”, each with their own independent set of Python packages installed in their site directories. A virtual environment is created on top of an existing Python installation, known as the virtual environment’s “base” Python, and may optionally be isolated from the packages in the base environment, so only those explicitly installed in the virtual environment are available.

## What were are making

In this lesson we're going to create:
* [color.py](color.py) - simple python script printing coloured output
* [requirements.txt](requirements.txt) - list of python packages our code needs
* [Makefile](Makefile) - `make` utility script to automate tasks (see [01. make basics](../01.%20make%20basics/) lesson)
  
## Base python

Find where the system python is installed:

```shell
$ readlink -f `which python3`
/opt/homebrew/Cellar/python@3.11/3.11.4_1/Frameworks/Python.framework/Versions/3.11/bin/python3.11
```

Check the version:

```shell
$ python -V
Python 3.11.4
```

See where the system python packages are installed:

```shell
$ python -c "import site; print(site.getsitepackages())"
['/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages']
```

So the packages installed to `/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages` (your system may have a different path) are common for all python programs you run.

## Create isolated python environments

Different python projects may require different incompatible versions of packages. To avoid installing and uninstalling packages to system `site-packages` directory, you can create isolated *virtual environments*.

1. Create project directory

   ```shell
   ~ $ mkdir myproject
   ~ $ cd myproject
   ```

2. Create the environment

   ```shell
   ~/myproject $ python3 -m venv venv
   ```

3. See that `venv` directory is created:

   ```shell
   ~/myproject $ ls -d */
    venv/
    ```
4. *Activate* the environment

    ```shell
    ~/myproject $ source venv/bin/activate
    (venv) ~/myproject $
    ```

5. See that `PATH` environment variable is updated and points to your `venv` first:

   ```shell
   (venv) ~/myproject $ echo $PATH
   /home/user/myproject/venv/bin:.....
   ```

6. See where the python is now:

    ```shell
    (venv) ~/myproject $ which python3
    /home/user/myproject/venv/bin/python3
    ```

7. See where the packages would be installed now:

   ```shell
   (venv) ~/myproject $ python3 -c "import site; print(site.getsitepackages())"
   /home/user/myproject/venv/lib/python3.11/site-packages
   ```

Now you can do whatever you want with this environment without affecting the base system.

## Installing packages
Let's say our project needs a coloured text output and uses an external `string-color` library for that:

```python
from stringcolor import cs

print(cs("жовтий", "yellow", "blue"))
print(cs("блакитний", "blue", "yellow"))
```

The library package should be installed:

```shell
(venv) ~/myproject $ pip install string-color
```

Very likely your project will install more than one library, you can install them all at once by telling pip to read the list from the file. Usual file name is `requirements.txt`:

```python
string-color
```

```shell
(venv) ~/myproject $ pip install -r requirements.txt
```

Let's see where the package is installed:

```shell
(venv) ~/myproject $ pip show string-color
Name: string-color
Version: 1.2.3
Summary: just another mod to print strings in 256 colors in the terminal.
Home-page: https://gitlab.com/shindagger/string-color
Author: Andy Klier
Author-email: andyklier@gmail.com
License: UNKNOWN
Location: /home/user/myproject/venv/lib/python3.11/site-packages
Requires: colorama, columnar, setuptools
Required-by: 
```

Also note, that installed package has version `1.2.3`. Library behaviour could change in future versions, so it is better to lock the required version when you install a package. Let's update `requirements.txt`:

```
string-color==1.2.3
```

## Automating tasks
For automation we're using `make` utility (see [01. make basics](../01.%20make%20basics/) lesson)

`make` operates with target files and the files they depend on. In our case the target would be `venv` directory with all the needed python packages installed. And it depends on content of `requirements.txt`. So the `Makefile` will look like:

```make
venv: requirements.txt
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
```

If add some more requirements, the `venv` rule would be executed again.

We may also add less cryptic alias to `venv`:

```make
.PHONY: setup
setup: venv
```

Also, remembering the good manners, we will add a clean-up:

```make
.PHONY: clean
clean:
    rm -rf venv
```

We can also run our script from the virtual environment without modifying our current shell variables, directly pointing to the python in virtual env:

```make
.PHONY: run
run: venv
    venv/bin/python color.py
```

```shell
$ make run
venv/bin/python3 color.py
жовтий
блакитний
```

## The result

* `color.py`:
  ```python
  from stringcolor import cs

  print(cs("жовтий", "yellow", "blue"))
  print(cs("блакитний", "blue", "yellow"))
  ```
* `requirements.txt`:
  ```text
  string-color==1.2.3
  ```
* `Makefile`:
  ```make
  venv: requirements.txt
      python3 -m venv venv
      venv/bin/pip install --upgrade pip
      venv/bin/pip install -r requirements.txt

  .PHONY: setup
   setup: venv

  .PHONY: run
  run:
      venv/bin/python3 color.py

  .PHONY: clean
  clean:
      rm -rf venv
  ```
