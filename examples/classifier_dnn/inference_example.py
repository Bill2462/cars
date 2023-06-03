import numpy as np
import tensorrt as trt
import pycuda.autoprimaryctx
import pycuda.driver as cuda
import time
from car.camera import CSICamera
from car.telemetry import TelemetrySender
import cv2

telemetry = TelemetrySender()
cam = CSICamera()

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
runtime = trt.Runtime(TRT_LOGGER)

host_inputs  = []
cuda_inputs  = []
host_outputs = []
cuda_outputs = []
bindings = []

def preprocess_image(img):
    mean = np.array([0.485, 0.456, 0.406]).astype('float32')
    stddev = np.array([0.229, 0.224, 0.225]).astype('float32')
    data = (np.asarray(img).astype('float32') / float(255.0) - mean) / stddev
    # Switch from HWC to to CHW order
    return np.moveaxis(data, 2, 0).astype(np.float32)

def prepare_engine(runtime):
    with open('efficient_net_b3.trt', 'rb') as f:
        buf = f.read()
        engine = runtime.deserialize_cuda_engine(buf)

    # create buffer
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        host_mem = cuda.pagelocked_empty(shape=[size], dtype=np.float32)
        cuda_mem = cuda.mem_alloc(host_mem.nbytes)

        bindings.append(int(cuda_mem))
        if engine.binding_is_input(binding):
            host_inputs.append(host_mem)
            cuda_inputs.append(cuda_mem)
        else:
            host_outputs.append(host_mem)
            cuda_outputs.append(cuda_mem)

    return engine

def inference(engine, context, stream, frame):
    np.copyto(host_inputs[0], frame.ravel())

    cuda.memcpy_htod_async(cuda_inputs[0], host_inputs[0], stream)
    context.execute_async(bindings=bindings, stream_handle=stream.handle)
    cuda.memcpy_dtoh_async(host_outputs[0], cuda_outputs[0], stream)
    stream.synchronize()

    output = host_outputs[0].reshape(np.concatenate(([1],engine.get_binding_shape(1))))
    return output

def main():
    engine = prepare_engine(runtime)
    context = engine.create_execution_context()
    stream = cuda.Stream()
    
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
    
    while 1:
        # time the inference
        start_time = time.time()
        frame = cam.read()

        # Frame size is 1920 x 1080 Resize and center crop so the resulting frame is 224x224 KEEP THE ASPECT RATIO
        frame = cv2.resize(frame, (398, 224))
        frame = frame[0:224, 87:311]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        telemetry.log_image("img", frame)
        batch = preprocess_image(frame)
        start_time = time.time()
        output = inference(engine, context, stream, batch)
        print(categories[np.argmax(output)])
        print("Inference time: %s seconds" % (time.time() - start_time))

if __name__ == '__main__':
    main()
