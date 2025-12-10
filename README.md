# colcon-python-project-uv

## Installation

Use this prototype
```bash
mkdir -p ~/colcon_extra_ws/src && cd ~/colcon_extra_ws
git clone https://github.com/colcon/colcon-python-project.git -b devel src/colcon-python-project
git clone https://github.com/Briancbn/colcon-python-project-uv.git -b feature/bn/add-venv-verb src/colcon-python-project-uv
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
mkdir colcon_ws/src -p
cd ~/colcon_ws
```

Download your python packages

First install additional dependencies
```bash
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
