import numpy as np
import tensorrt as trt
import pycuda.autoprimaryctx
import pycuda.driver as cuda
import cv2

def get_top_k(logits, k):
    return logits.argsort()[-k:][::-1]

def softmax(x):
    x = np.squeeze(x)
    return np.exp(x) / np.sum(np.exp(x))

def resize_and_crop(img):
    img = cv2.resize(img, (398, 224))
    img = img[0:224, 87:311]
    return img

def preprocess_image(img):
    mean = np.array([0.485, 0.456, 0.406]).astype(np.float32)
    stddev = np.array([0.229, 0.224, 0.225]).astype(np.float32)
    data = (np.asarray(img).astype(np.float32) / float(255.0) - mean) / stddev
    return np.moveaxis(data, 2, 0).astype(np.float16) # Switch from HWC to to CHW order

def load_classes(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f.readlines()]

class ImageClassifier:
    def __init__(self, engine_filepath):
        TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
        self.runtime = trt.Runtime(TRT_LOGGER)
        
        self._load_engine(engine_filepath)

        self.context = self.engine.create_execution_context()
        self.stream = cuda.Stream()
    
    def _load_engine(self, filepath):
        self.host_inputs  = []
        self.cuda_inputs  = []
        self.host_outputs = []
        self.cuda_outputs = []
        self.bindings = []

        with open(filepath, 'rb') as f:
            buf = f.read()
            self.engine = self.runtime.deserialize_cuda_engine(buf)
        
        for binding in self.engine:
            size = trt.volume(self.engine.get_binding_shape(binding)) * self.engine.max_batch_size
            host_mem = cuda.pagelocked_empty(shape=[size], dtype=np.float16)
            cuda_mem = cuda.mem_alloc(host_mem.nbytes)

            self.bindings.append(int(cuda_mem))
            if self.engine.binding_is_input(binding):
                self.host_inputs.append(host_mem)
                self.cuda_inputs.append(cuda_mem)
            else:
                self.host_outputs.append(host_mem)
                self.cuda_outputs.append(cuda_mem)
        

    def inference(self, image):
        np.copyto(self.host_inputs[0], image.ravel())
        
        cuda.memcpy_htod_async(self.cuda_inputs[0], self.host_inputs[0], self.stream)
        self.context.execute_async(bindings=self.bindings, stream_handle=self.stream.handle)
        cuda.memcpy_dtoh_async(self.host_outputs[0], self.cuda_outputs[0], self.stream)
        self.stream.synchronize()

        output = self.host_outputs[0].reshape(np.concatenate(([1], self.engine.get_binding_shape(1))))
        return output



