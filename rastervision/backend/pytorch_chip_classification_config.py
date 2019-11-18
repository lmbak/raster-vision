from copy import deepcopy

import rastervision as rv

from rastervision.backend.pytorch_chip_classification import (
    PyTorchChipClassification)
from rastervision.backend.simple_backend_config import (
    SimpleBackendConfig, SimpleBackendConfigBuilder)
from rastervision.backend.api import PYTORCH_CHIP_CLASSIFICATION


class TrainOptions():
    def __init__(self,
                 batch_size=None,
                 lr=None,
                 one_cycle=None,
                 num_epochs=None,
                 model_arch=None,
                 sync_interval=None,
                 debug=None,
                 log_tensorboard=None,
                 run_tensorboard=None,
                 equalize=None):
        self.batch_size = batch_size
        self.lr = lr
        self.one_cycle = one_cycle
        self.num_epochs = num_epochs
        self.model_arch = model_arch
        self.sync_interval = sync_interval
        self.debug = debug
        self.log_tensorboard = log_tensorboard
        self.run_tensorboard = run_tensorboard
        self.equalize = equalize

    def __setattr__(self, name, value):
        if name in ['batch_size', 'num_epochs', 'sync_interval']:
            value = int(value) if isinstance(value, float) else value
        super().__setattr__(name, value)


class PyTorchChipClassificationConfig(SimpleBackendConfig):
    train_opts_class = TrainOptions
    backend_type = PYTORCH_CHIP_CLASSIFICATION
    backend_class = PyTorchChipClassification


class PyTorchChipClassificationConfigBuilder(SimpleBackendConfigBuilder):
    config_class = PyTorchChipClassificationConfig

    def _applicable_tasks(self):
        return [rv.CHIP_CLASSIFICATION]

    def with_train_options(self,
                           batch_size=8,
                           lr=1e-4,
                           one_cycle=True,
                           num_epochs=1,
                           model_arch='resnet18',
                           sync_interval=1,
                           debug=False,
                           log_tensorboard=True,
                           run_tensorboard=True,
                           equalize=False):
        """Set options for training models.

        Args:
            batch_size: (int) the batch size
            weight_decay: (float) the weight decay
            lr: (float) the learning rate if using a fixed LR
                (ie. one_cycle is False),
                or the maximum LR to use if one_cycle is True
            one_cycle: (bool) True if cyclic learning rate scheduler should
                be used. This
                cycles the LR once during the course of training and seems to
                result in a pretty consistent improvement. See lr for more
                details.
            num_epochs: (int) number of epochs (sweeps through training set) to
                train model for
            model_arch: (str) Any classification model option in
                torchvision.models is valid, for example, resnet18.
            sync_interval: (int) sync training directory to cloud every
                sync_interval epochs.
            debug: (bool) if True, save debug chips (ie. visualizations of
                input to model during training) during training and use
                single-core for creating minibatches.
            log_tensorboard: (bool) if True, write events to Tensorboard log
                file
            run_tensorboard: (bool) if True, run a Tensorboard server at
                port 6006 that uses the logs generated by the log_tensorboard
                option
            equalize: (bool) if True, the data will be sampled such that each
                class occurs with the same probability. So if we have class A
                with 120 images and class B with 50 images, the training will be
                performed on 240 images (amount_of_images_in_largest_class *
                amount_of_classes). All 120 images from class A will be used
                exactly once. All images off class B will be used at least 2 times.
                The 20 remaining images will be randomly sampled for the initial 50.
                The exact images used remain constant throughout the epochs.
        """
        b = deepcopy(self)
        b.train_opts = TrainOptions(
            batch_size=batch_size,
            lr=lr,
            one_cycle=one_cycle,
            num_epochs=num_epochs,
            model_arch=model_arch,
            sync_interval=sync_interval,
            debug=debug,
            log_tensorboard=log_tensorboard,
            run_tensorboard=run_tensorboard,
            equalize=equalize)
        return b

    def with_pretrained_uri(self, pretrained_uri):
        """pretrained_uri should be uri of exported model file."""
        return super().with_pretrained_uri(pretrained_uri)
