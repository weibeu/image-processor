from abc import ABC, abstractmethod


class ImageFunction(ABC):

    @abstractmethod
    def _process(self):
        raise NotImplementedError
