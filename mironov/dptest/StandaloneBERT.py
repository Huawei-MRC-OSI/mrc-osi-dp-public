# Applied model defined by
# https://github.com/CyberZHG/keras-bert/blob/master/demo/tune/keras_bert_classification_tpu.ipynb
# to DeepPavlov

import os
os.environ['TF_KERAS'] = '1'

import numpy as np
import ipdb
import codecs
import tensorflow as tf
import ipdb

def _trace():
  ipdb.set_trace()

from deeppavlov import build_model, train_model, configs
from deeppavlov.core.commands.utils import expand_path, import_packages, parse_config
from deeppavlov.core.commands.train import read_data_by_config, get_iterator_from_config
from deeppavlov.core.common.registry import get_model, register
from deeppavlov.core.models.nn_model import NNModel
from deeppavlov.core.models.component import Component
from deeppavlov.core.models.lr_scheduled_model import LRScheduledModel
from deeppavlov.dataset_readers.imdb_reader import ImdbReader
from deeppavlov.download import deep_download

from tqdm import tqdm
from tensorflow.python import keras
from keras_bert import AdamWarmup, calc_train_steps
from keras_bert import load_trained_model_from_checkpoint, Tokenizer
from keras_radam import RAdam

from logging import getLogger
from typing import List,Any,Optional
from pathlib import Path

log = getLogger(__name__)

@register('StandaloneBERT')
class StandaloneBERT(NNModel):

  def __init__(self, *args, **kwargs)->None:
    print('StandaloneBERT created', str(args), str(kwargs))

    log.warn(f"{args}")
    log.warn(kwargs)
    seq_len = int(kwargs['seq_len'])
    learning_rate = float(kwargs['learning_rate'])
    pretrained_path = Path(kwargs['bert_models']).expanduser()
    config_path = pretrained_path / 'bert_config.json'
    checkpoint_path = pretrained_path / 'bert_model.ckpt'
    vocab_path = pretrained_path / 'vocab.txt'

    print(f"Creating Keras-BERT model")
    model = load_trained_model_from_checkpoint(
      str(config_path),
      str(checkpoint_path),
      training=True,
      trainable=True,
      seq_len=seq_len)

    inputs = model.inputs[:2]
    bert_outputs = model.get_layer('NSP-Dense').output
    head_outputs = keras.layers.Dense(units=2, activation='softmax')(bert_outputs)

    model = keras.Model(inputs, head_outputs)
    model.compile(
      RAdam(lr=learning_rate),
      loss='sparse_categorical_crossentropy',
      metrics=['sparse_categorical_accuracy'],
    )

    print(f"Preparing Keras-BERT Tokenizer")
    token_dict:dict = {}
    with codecs.open(str(vocab_path), 'r', 'utf8') as reader:
      for line in reader:
        token = line.strip()
        token_dict[token] = len(token_dict)

    tokenizer = Tokenizer(token_dict)

    self.model = model
    self.name = 'StandaloneBert_imdb'
    self.tokenizer:Tokenizer = tokenizer
    self.load_path:Path = Path(kwargs.get('load_path',''))
    self.save_path:Path = Path(kwargs['save_path'])
    self.seq_len = seq_len

    if len(str(self.load_path))>0:
      self.load()

  def destroy(self)->None:
    print('StandaloneBERT::destroy called')
    if hasattr(self,'model'):
      delattr(self,'model')
    super().destroy()
    keras.backend.clear_session()

  def _train(self, texts:List[str], true_label_ids:List[List[int]])->None:
    print('T', end='', flush=True);

    token_ids=[]
    label_ids=[]
    for text,label in zip(texts,true_label_ids):
      tokens,segments = self.tokenizer.encode(text, max_len=self.seq_len)
      token_ids.append(tokens)
      label_ids.append(label[0])

    indices=np.array(token_ids)
    sentiments=np.array(label_ids)
    self.model.train_on_batch(x=[indices, np.zeros_like(indices)], y=sentiments)
    pass

  def _infer(self, texts:List[str], *args) -> List[List[float]]:
    print('.', end='', flush=True)

    indices=[]
    for text in texts:
      ids,segments = self.tokenizer.encode(text, max_len=self.seq_len)
      indices.append(ids)
    indices=np.array(indices)

    results = self.model.predict([indices, np.zeros_like(indices)])
    return results.tolist()

  def process_event(self, event_name, data):
    # print('StandaloneBERT::process_event called, event', event_name)
    pass

  def save(self, *args, **kwargs)->None:
    print('StandaloneBERT::save')

    save_path = expand_path((self.save_path / self.name).with_suffix('.h5'))

    print(f"Saving to {save_path}")
    save_path.parent.mkdir(parents=True, exist_ok=True)

    try:
      self.model.save_weights(str(save_path))
    except ValueError as err:
      log.warn(f"Failed to save model weights. Error is {err}")

  def load(self, *args, **kwargs)->None:
    print('StandaloneBERT::load',)

    if self.load_path is None:
      raise RuntimeError(f'Load path is not set for {self.name}')

    load_path = expand_path((self.load_path / self.name).with_suffix('.h5'))
    print(f"Loading from {load_path}")

    try:
      self.model.load_weights(str(load_path))
    except ValueError as err:
      log.warn(f"Failed to load model weights. Error is {err}")
    except OSError as err:
      log.warn(f"Failed to load model weights. Error is {err}")

  def train_on_batch(self, *args, **kwargs):
    return self._train(*args, **kwargs)

  def __call__(self, *args, **kwargs):
    return self._infer(*args, **kwargs)




class DPModel:
  iterator:Any
  data:Any
  config:Any
  def __init__(self)->None:
    pass

def load(m:DPModel)->None:
  m.config = parse_config(os.environ.get('MRCNLP_ROOT','/workspace') + "/mironov/dptest/StandaloneBERT.json")
  deep_download(m.config)

  import_packages(m.config.get('metadata', {}).get('imports', []))
  m.data = read_data_by_config(m.config)


def train(m:DPModel):
  """ Use the generic algorithm of `train_evaluate_model_from_config`, but
  shrink its scope to the particular task-specific config. This should allow us
  to run the model, defined outside the DP tree, using config defined outside DP
  tree. """

  m.iterator = get_iterator_from_config(m.config, m.data)

  def _check_set(cfg, fld, val):
    if fld not in cfg:
      cfg.update({fld : val})
    else:
      print(f"{cfg}.{fld} is already set to {cfg[fld]}")

  train_config = m.config['train']
  eval_config = train_config['evaluation_targets']
  chainer_config = m.config['chainer']

  _check_set(train_config, 'start_epoch_num', 0)
  trainer = get_model(train_config.pop('class_name', 'nn_trainer'))\
                     (chainer_config=chainer_config, **train_config)

  trainer.train(m.iterator)
  trainer._loaded = False # Force model re-creation

  res = trainer.evaluate(m.iterator, eval_config, print_reports=True)
  return res

def run()->None:
  m=DPModel()
  load(m)
  train(m)


