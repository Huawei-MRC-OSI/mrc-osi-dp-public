DeepPavlov as a training library
--------------------------------

In this repository we demonstrate how to re-use [DeepPavlov](https://deeppavlov.ai/)
infrastructure for training custom NLP models.

Specifically, we wrap popular
[CyberZHG/Keras-bert](https://github.com/CyberZHG/keras-bert) model with
DeepPavlov dataset reader and train it using NN-trainer on [Imdb-Sentiment
task](http://ai.stanford.edu/~amaas/data/sentiment/).  No modification of DP
source tree is required.

In this example we show how to:

* Use a custom third-party model with the DeepPavlov framework
* Re-use rich collection of dataset readers from DeepPavlov
* Limit the Model-Framework interface up to a small maintainable API.

_Note: we depend on unmerged PR <https://github.com/deepmipt/DeepPavlov/pull/962>
which adds a task-specific dataset reader to the DeepPavlov. It doesn't affect
the overall approach_

Working with the repository
---------------------------

We use Docker environment in this project. To open the development shell:

1. Download git-submodules with `git submodule update --init
   --recursive`.
2. Run `rundocker.sh ./docker/mironov.docker [-n]`
3. By default, docker image maps certain TCP ports to allow connecting to
   Jupyter or Tensorboard servers that may be run within the container (note,
   they have to be started explicitly).  `./rundocker.sh` accepts
   `--no-map-sockets|-n` flag to disable this feature e.g. to avoid port
   conflicts.

The current setup mounts project's root directory into container's /home. It is
thus possible to edit code using your favorite host's editor and compile it with
CLI tools installed in the Docker container.

_Note: Docker image presented here contains custom SSL certificates that we need
in our regular work. Don't use this image for security-critical tasks!_

Running the training example
----------------------------

Once you run docker image and enter development shell, you could do the
following:

1. To run the training example from the ipython, do the following
   ```
   $ ipython
   > from dptest.StandaloneBERT import *
   > run()
   ```

2. Run the model training example using python
   ```
   $ python -m 'dptest.StandaloneBERT'
   ```

Notes
-----

* [StandaloneBERT.json](./mironov/dptest/StandaloneBERT.json) declares the DeepPavlov
  model configuration.
  - `StandaloneBERT` is a custom component defined in
    [StandaloneBERT.py](./mironov/StandaloneBERT.py) file.
  - Other Chainer components are re-used.
* [StandaloneBERT.py](./mironov/dptest/StandaloneBERT.py) defines the model wrapper and
  its initialization.
* The Main function's logic is implemented in `load` and `train` functions. They loosely
  follow the algorithm of DeepPavlov's `train_evaluate_model_from_config`, but
  are shorter since we removed task-irrelevant branches.

