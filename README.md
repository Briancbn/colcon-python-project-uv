# colcon-python-project-uv

THIS IS A PROTOTYPE!!

This package provides the following functions
- extend `colcon-python-project` to use `uv` executable instead of PyPI `uv_build` to build colcon packages
- add support for `UV` workspace.
- add a `venv` verb to sync non-local PyPI dependency using `uv`

## Installation

Install additional python dependencies
```bash
sudo apt install python3-tomli-w
```

Install this prototype from source
```bash
mkdir -p ~/colcon_extra_ws/src && cd ~/colcon_extra_ws
git clone https://github.com/colcon/colcon-python-project.git -b devel src/colcon-python-project
git clone https://github.com/Briancbn/colcon-python-project-uv.git -b devel src/colcon-python-project-uv
colcon build
. install/local_setup.sh
```

## Usage

Use this for another workspace

First install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create a colcon workspace

```bash
mkdir ~/colcon_ws/src -p
```

Download your python packages into `colcon_ws/src`

First install additional PyPI dependencies to virtual environment
```bash
cd ~/colcon_ws
colcon venv sync
```

Build the rest of the packages
```bash
colcon build
```

Source the workspace
```bash
. install/setup.bash
```

Activate the virtual environment containing the additional PyPI dependencies.
```bash
. install/activate.sh
```

Deactivate the python virtual environment
```bash
deactivate_all
```

## Explanation

If the `pyproject.toml`'s `build-system.build-backend` is not `uv_build`, colcon will fallback to using `colcon-python-project` to build.

To check this, run `colcon list`

```
my_poetry_package	  src/my_poetry_package	   (python.project)       <-- not using UV
my_uv_package       src/my_uv_package	     (python.project.uv)
```

`colcon venv sync` only install dependencies that cannot found locally within the workspace.
After success, `install/.uv_python_project_venv/.venv` is created, together with a custom activation script.

```bash
. install/setup.bash
. install/activate.sh
echo $PYTHONPATH | sed "s/:/\n/g"
```

You should be able to find a line like the following
```
<...>/install/.uv_python_project_venv/.venv/lib/python3.x/site-packages
```

To deactivate, and check the venv path is removed
```bash
deactivate_all
echo $PYTHONPATH | sed "s/:/\n/g"
```
