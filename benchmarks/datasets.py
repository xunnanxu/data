from torchvision import transforms, datasets
import torch
from abc import ABC, abstractmethod

class DataPipeReadyBenchmark(ABC):
    @abstractmethod
    def prepare_pipe(self, params):
        return NotImplementedError

class GTSRBReadyBenchmark(DataPipeReadyBenchmark):
    def transform(img):
        t= transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(size=(100,100)),
            transforms.ToTensor()]
        )
        return t(img)

    def str_to_list(str):
        l = []
        for char in str:
            l.append(int(char))
        return l

    def prepare_pipe(self, params):
        batch_size, device, dp = params
        # Filter out bounding box and path to image
        dp = dp.map(lambda sample : {"image" : sample["image"], "label" : sample["label"]})

        # Apply image preprocessing
        dp = dp.map(lambda sample : transform(sample.decode().to(torch.device(device))), input_col="image")
        dp = dp.map(lambda sample : torch.tensor(str_to_list(sample.to_categories())).to(torch.device(device)), input_col="label")

        # Batch
        dp = dp.batch(batch_size)
        return dp    
    
class HuggingFaceReadyBenchmark(DataPipeReadyBenchmark):
    def prepare(self, dataset_name):
        return NotImplementedError