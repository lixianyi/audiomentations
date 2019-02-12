import random


class Compose:
    def __init__(self, transforms, p=1.0):
        self.transforms = transforms
        self.p = p

    def __call__(self, samples, sample_rate):
        if random.random() < self.p:
            for transform in self.transforms:
                samples = transform(samples, sample_rate)

        return samples
