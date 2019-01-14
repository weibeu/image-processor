from abc import ABC, abstractmethod


class ImageFunction(ABC):

    FONT_PATH = "app/core/image/templates/fonts/"

    @abstractmethod
    def _process(self):
        raise NotImplementedError
