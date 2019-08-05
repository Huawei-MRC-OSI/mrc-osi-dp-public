import numpy as np

from deeppavlov import build_model, train_model, configs
from deeppavlov.core.commands.utils import expand_path, import_packages, parse_config
from deeppavlov.core.commands.train import read_data_by_config, get_iterator_from_config
from deeppavlov.core.common.registry import get_model, register
from deeppavlov.core.models.nn_model import NNModel
from deeppavlov.core.models.lr_scheduled_model import LRScheduledModel

from typing import List,Any

# def train_simple():
#   """ Train the model defined in DP tree, using a config defined in DP tree."""
#   # model = build_model(configs.snips.snips, download=True)
#   # train_model(configs.classifiers.insults_kaggle)
#   m = train_model(configs.snips.snips)
#   model = build_model(configs.squad.squad, download=True)
#   train_model(model)


@register('StandaloneModel')
class StandaloneModel(LRScheduledModel):
  def __init__(self, *args, **kwargs):
    print('StandaloneModel created')

  def train_on_batch(self, x:List[Any], y_intent_ids:List[Any], y_slot_ids:List[Any]):
    print('StandaloneModel::train_on_batch called')
    print('StandaloneModel ===> X', 'len', len(x), 'data', x)
    print('StandaloneModel ===> YI', 'len', len(y_intent_ids), 'data', y_intent_ids)
    print('StandaloneModel ===> YS', 'len', len(y_slot_ids), 'data', y_slot_ids)
    pass

  def process_event(self, event_name, data):
    print('StandaloneModel::process_event called, event', event_name)
    pass

  def save(self):
    print('StandaloneModel::save')

  def __call__(self, data: List[List[np.ndarray]], *args) -> List[List[float]]:
    print('StandaloneModel::__call__ called')
    return list(map(lambda words: [0.0], data))


def train_standalone():
  """ Use the generic algorithm of `train_evaluate_model_from_config`, but
  shrink its scope to the particular task-specific config. This should allow us
  to run the model, defined outside the DP tree, using config defined outside DP
  tree. """

  config = parse_config("mironov/dptest/Standalone.json")

  import_packages(config.get('metadata', {}).get('imports', []))
  data = read_data_by_config(config)
  iterator = get_iterator_from_config(config, data)

  train_config = config['train']
  train_config.update({'start_epoch_num' : 0})
  evaluation_targets = train_config['evaluation_targets']
  trainer_class = get_model(train_config.pop('class_name', 'nn_trainer'))
  trainer = trainer_class(config['chainer'], **train_config)

  trainer.train(iterator)
  trainer.get_chainer().destroy()

  res = trainer.evaluate(iterator, evaluation_targets, print_reports=True)
  return res

