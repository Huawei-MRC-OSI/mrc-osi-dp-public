#!/bin/sh

# Below deps were obtained by running `./mironov/dptest/checkdeps.sh`
# Note: `./install_git_hack.sh` may be needed, or TLS error may prevent Git from
# working.

pip3 install python-aiml==0.9.1
pip3 install git+https://github.com/deepmipt/bert.git@feat/multi_gpu
pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz#egg=en_core_web_sm==2.1.0
pip3 install pybind11==2.2.3 git+https://github.com/deepmipt/fastText.git#egg=fastText==0.8.22
pip3 install gensim==3.7.3
pip3 install git+https://github.com/kpu/kenlm.git@2ad7cb56924cd3c6811c604973f592cb5ef604eb#egg=kenlm
pip3 install russian-tagsets==0.6
pip3 install spacy==2.1.3
pip3 install lxml==4.3.4 python-Levenshtein==0.12.0 sortedcontainers==2.0.2
# pip3 install tensorflow-gpu==1.14.0
# pip3 install tensorflow-hub==0.1.1
