if test -z "$MRCNLP_ROOT" ; then
  export MRCNLP_ROOT=`pwd`
fi
export CWD="$MRCNLP_ROOT"
export TERM=xterm-256color
export PATH=$MRCNLP_ROOT/.nix_docker_inject.env/bin:$PATH
export PYTHONPATH="" # /usr/local/lib/python3.6/dist-packages
export MYPYPATH=""
for p in \
  $MRCNLP_ROOT/mironov/tensorflow-sys \
  $MRCNLP_ROOT/mironov/parlai \
  $MRCNLP_ROOT/mironov/tensor2tensor \
  $MRCNLP_ROOT/mironov/keras-bert \
  $MRCNLP_ROOT/mironov/keras-radam \
  $MRCNLP_ROOT/mironov/DeepPavlov \
  $MRCNLP_ROOT/mironov/seq2seq \
  $MRCNLP_ROOT/mironov \
   ; do
  if test -d "$p" ; then
    export PYTHONPATH="$p:$PYTHONPATH"
    export MYPYPATH="$p:$MYPYPATH"
  else
    echo "Directory '$p' doesn't exists. Not adding to PYTHONPATH" >&2
  fi
done

alias ipython="sh $MRCNLP_ROOT/ipython.sh"

if test -f $MRCNLP_ROOT/.nix_docker_inject.env/etc/myprofile ; then
  . $MRCNLP_ROOT/.nix_docker_inject.env/etc/myprofile
fi

runjupyter() {
  jupyter-notebook --ip 0.0.0.0 --port 8888 \
    --NotebookApp.token='' --NotebookApp.password='' "$@" --no-browser
}
alias jupyter=runjupyter

runtensorboard() {(
  mkdir $MRCNLP_ROOT/_logs 2>/dev/null
  echo "Tensorboard logs redirected to $MRCNLP_ROOT/_logs/tensorboard.log"
  if test -n "$1" ; then
    args="--logdir $1"
    shift
  else
    args="--logdir $MRCNLP_ROOT/_logs"
  fi
  tensorboard $args "$@" >"$MRCNLP_ROOT/_logs/tensorboard.log" 2>&1
) & }

runchrome() {(
  mkdir -p $HOME/.chrome_mrc-nlp || true
  chromium \
    --user-data-dir=$HOME/.chrome_mrc-nlp \
    --explicitly-allowed-ports=`seq -s , 6000 1 6020`,`seq -s , 8000 1 8020`,7777 \
    http://127.0.0.1:`expr 6000 + $UID - 1000` "$@"
)}

e() {(
  if test -x "$EDITOR"; then
    $EDITOR "$@"
  else
    echo "EDITOR is not executable" >&2
  fi
)}


docnews() {
  ndays="$1"
  test -z "$ndays" && ndays=3
  rev=$(git log -1 --before=@{"$ndays".days.ago} --format=%H)
  docs=`git diff --name-status  --oneline "$rev" | grep -v '^D' | grep -E 'doc|\.md$' | awk '{print $2}'`
  git diff "$rev" -- $docs
}

runomniboard() {(
  db_name="$1"
  mkdir $MRCNLP_ROOT/_logs 2>/dev/null
  echo "Omniboard logs redirected to $MRCNLP_ROOT/_logs/omniboard.log"
  omniboard -m "172.17.0.1:27017:$db_name" >"$MRCNLP_ROOT/_logs/omniboard.log" 2>&1
)& }

cudarestart() {
  sudo rmmod nvidia_uvm ; sudo modprobe nvidia_uvm
}

runnetron() {
  netron --host 0.0.0.0 -p 6006 "$@"
}
