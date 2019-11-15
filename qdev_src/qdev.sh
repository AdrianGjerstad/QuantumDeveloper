#!/usr/bin/bash

# Quantum Developer Shell Script for Linux/Unix Distros

function __qdev-log-shell() {
  echo '<'$blue'shell'$normal'> ['$bold$(date +'%Y-%m-%dT%H:%M:%SZ%z')$normal'] ['$1']: '$2
}

function qdev() {

  stty -echo
  
  if test -t 1; then
    ncolors=$(tput colors)
  
    if test -n "$ncolors" && test $ncolors -ge 8; then
      bold="$(tput bold)"
      underline="$(tput smul)"
      standout="$(tput smso)"
      normal="$(tput sgr0)"
      black="$(tput setaf 0)"
      red="$(tput setaf 1)"
      green="$(tput setaf 2)"
      yellow="$(tput setaf 3)"
      blue="$(tput setaf 4)"
      magenta="$(tput setaf 5)"
      cyan="$(tput setaf 6)"
      white="$(tput setaf 7)"
    fi
  fi
  
  __qdev-log-shell $blue'INF'$normal 'Checking status...'

  command python3 -V>/dev/null 2>&1

  if [[ $? -eq 127 ]]; then
    __qdev-log-shell $red'ERR'$normal "Python3 not installed at \`python3'. Aborting..."
    stty echo
    return 100
  fi

  # Loop through $PATH to find src location
  while read -d ':' p; do
    # $p is the splitted path to check

    if [[ -f $p/qdev_src/qdev_magic.txt ]]; then
      export _QDEV_SRC=$p/qdev_src
      break
    fi
  done <<< $PATH:
  
  if [[ $_QDEV_SRC == '' ]]; then
    __qdev-log-shell $red'ERR'$normal 'Quantum Developer source code directory could not be found in $PATH. Aborting...'
    stty echo
    return 101
  fi

  __qdev-log-shell $blue'INF'$normal 'Status checks succeeded.'
  __qdev-log-shell $blue'INF'$normal 'Starting Quantum Developer script.'

  python3 $_QDEV_SRC/main.py $@

  unset _QDEV_SRC
  
  stty echo
  read -t 1 -n 10000 discard
  return 0
}

