_colcon_prepend_unique_value() {
  # arguments
  _listname="$1"
  _value="$2"

  # get values from variable
  eval _values=\"\$$_listname\"
  # backup the field separator
  _colcon_prepend_unique_value_IFS=$IFS
  IFS=":"
  # start with the new value
  _all_values="$_value"

  # TODO(anyone): add support for zsh
  # # workaround SH_WORD_SPLIT not being set in zsh
  # if [ "$(command -v colcon_zsh_convert_to_array)" ]; then
  #   colcon_zsh_convert_to_array _values
  # fi

  # iterate over existing values in the variable
  for _item in $_values; do
    # ignore empty strings
    if [ -z "$_item" ]; then
      continue
    fi
    # ignore duplicates of _value
    if [ "$_item" = "$_value" ]; then
      continue
    fi
    # keep non-duplicate values
    _all_values="$_all_values:$_item"
  done
  unset _item
  # restore the field separator
  IFS=$_colcon_prepend_unique_value_IFS
  unset _colcon_prepend_unique_value_IFS
  # export the updated variable
  eval export $_listname=\"$_all_values\"
  unset _all_values
  unset _values

  unset _value
  unset _listname
}


# since a plain shell script can't determine its own path when being sourced
# either use the provided COLCON_VENV_PREFIX
# or fall back to the build time prefix (if it exists)
_colcon_activate_sh_COLCON_VENV_PREFIX="@(venv_path)"
if [ -z "$COLCON_VENV_PREFIX" ]; then
  if [ ! -d "$_colcon_activate_sh_COLCON_VENV_PREFIX" ]; then
    echo "The build time path \"$_colcon_activate_sh_COLCON_VENV_PREFIX\" doesn't exist. Either source a script for a different shell or set the environment variable \"COLCON_VENV_PREFIX\" explicitly." 1>&2
    unset _colcon_activate_sh_COLCON_VENV_PREFIX
    return 1
  fi
  COLCON_VENV_PREFIX="$_colcon_activate_sh_COLCON_VENV_PREFIX"
fi
unset _colcon_activate_sh_COLCON_VENV_PREFIX

# function to source another script with conditional trace output
# first argument: the path of the script
# additional arguments: arguments to the script
_colcon_activate_sh_source_script() {
  if [ -f "$1" ]; then
    if [ -n "$COLCON_TRACE" ]; then
      echo "# . \"$1\""
    fi
    . "$@@"
  else
    echo "not found: \"$1\"" 1>&2
  fi
}

# source sh hooks
_colcon_activate_sh_source_script "$COLCON_VENV_PREFIX/bin/activate"

_colcon_prepend_unique_value PYTHONPATH "@(python_lib_path)"

# override deactivate command
deactivate_all() {
  if [ "$(command -v deactivate)" ]; then
    deactivate "$@@"
  fi

  _colcon_venv_delete_value() {
    # arguments
    _listname="$1"
    _value="$2"
  
    # get values from variable
    eval _values=\"\$$_listname\"
    # backup the field separator
    _colcon_delete_unique_value_IFS=$IFS
    IFS=":"
    # start with no value
    _all_values=""
  
    # TODO(anyone): add support for zsh
    # # workaround SH_WORD_SPLIT not being set in zsh
    # if [ "$(command -v colcon_zsh_convert_to_array)" ]; then
    #   colcon_zsh_convert_to_array _values
    # fi
  
    # iterate over existing values in the variable
    for _item in $_values; do
      # ignore empty strings
      if [ -z "$_item" ]; then
        continue
      fi
      # ignore duplicates of _value
      if [ "$_item" = "$_value" ]; then
        continue
      fi
      # keep non-duplicate values
      _all_values="$_all_values:$_item"
    done
    unset _item
    # restore the field separator
    IFS=$_colcon_delete_unique_value_IFS
    unset _colcon_delete_unique_value_IFS
    # export the updated variable
    eval export $_listname=\"$_all_values\"
    unset _all_values
    unset _values
  
    unset _value
    unset _listname
  }

  _colcon_venv_delete_value PYTHONPATH "@(python_lib_path)"

  if [ ! "${1-}" = "nondestructive" ] ; then
    # Self destruct!
    unset -f deactivate_all
    unset -f _colcon_delete_value
    unset COLCON_VENV_PREFIX
  fi
}

unset _colcon_activate_sh_source_script
unset _colcon_prepend_unique_value
