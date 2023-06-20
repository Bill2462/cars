import torchvision.models as models
import torch
import torch.onnx

model = models.efficientnet_b3(pretrained=True).eval()

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "efficient_net_b3.onnx")
