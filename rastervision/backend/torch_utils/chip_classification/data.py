from os.path import join

from torchvision.transforms import Compose, ToTensor
from torch.utils.data import DataLoader
from torch.utils.data.sampler import WeightedRandomSampler

from rastervision.backend.torch_utils.data import DataBunch
from rastervision.backend.torch_utils.chip_classification.folder import (
    ImageFolder, equalize_classes_through_oversampling)

def build_databunch(equalize, data_dir, img_sz, batch_sz, class_names):
    num_workers = 4

    train_dir = join(data_dir, 'train')
    valid_dir = join(data_dir, 'valid')

    aug_transform = Compose([ToTensor()])
    transform = Compose([ToTensor()])

    train_ds = ImageFolder(
        train_dir, transform=aug_transform, classes=class_names)
    valid_ds = ImageFolder(valid_dir, transform=transform, classes=class_names)

    if equalize == True:
        train_ds.samples = equalize_classes_through_oversampling(
            classes = train_ds.classes,
            class_to_idx = train_ds.class_to_idx,
            samples = train_ds.samples
        )

        valid_ds.samples = equalize_classes_through_oversampling(
            classes = valid_ds.classes,
            class_to_idx = valid_ds.class_to_idx,
            samples = valid_ds.samples
        )

    train_dl = DataLoader(
        train_ds,
        shuffle=True,
        batch_size=batch_sz,
        num_workers=num_workers,
        drop_last=True,
        pin_memory=True)
    valid_dl = DataLoader(
        valid_ds,
        batch_size=batch_sz,
        num_workers=num_workers,
        pin_memory=True)

    return DataBunch(train_ds, train_dl, valid_ds, valid_dl, class_names)
