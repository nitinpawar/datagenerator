#!/bin/bash

numBatches=4
totalrows=1000000
rowsInEachJoin=`echo $totalrows / $numBatches| bc`
staging_dir=datagen_temp_batcher

debug() { echo "DEBUG: $*" >&2; }
waitall() { # PID...
  ## Wait for children to exit and indicate whether all exited with 0 status.
  local errors=0
  while :; do
    debug "Processes remaining: $*"
    for pid in "$@"; do
      shift
      if kill -0 "$pid" 2>/dev/null; then
        debug "$pid is still alive."
        set -- "$@" "$pid"
      elif wait "$pid"; then
        debug "$pid exited with zero exit status."
      else
        debug "$pid exited with non-zero exit status."
        ((++errors))
      fi
    done
    (("$#" > 0)) || break
    # TODO: how to interrupt this sleep when a child terminates?
    sleep ${WAITALL_DELAY:-1}
   done
  ((errors == 0))
}


pids=""
for (( i=1; i<=$numBatches; i++ ))
do
	./gendata.py -i definition -r 2500 -d tempdata -t 10 &
	pids="$pids $!"	
done

waitall $pids

