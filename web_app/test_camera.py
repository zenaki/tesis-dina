import os, time, cv2, torch, torch.backends.cudnn as cudnn
import numpy as np

# from models.experimental import attempt_load
# from utils.general import set_logging, check_img_size, check_imshow, non_max_suppression, scale_coords, xyxy2xywh
# from utils.torch_utils import select_device, time_synchronized
# from utils.datasets import LoadStreams, letterbox
# from utils.plots import plot_one_box

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages, letterbox
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

cap = cv2.VideoCapture(0)

video_source = 0
weights = "../model_20210516.pt"    # model.pt path(s)
img_size = 640                         # inference size (pixels)
conf_thres = 0.25                   # object confidence threshold
iou_thres = 0.45                    # IOU threshold for NMS

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) % 100
    
    # Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(img_size, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Set Dataloader
    # view_img = check_imshow()
    view_img = True
    cudnn.benchmark = True  # set True to speed up constant image size inference
    # dataset = LoadStreams(video_source, img_size=imgsz, stride=stride)
    # dataset = cv2.VideoCapturevideo_source)
    
    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]
    
    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    
    _, imgs = cap.read()  # guarantee first frame
    n = 0
    while cap.isOpened():
        n += 1
        cap.grab()
        if n == 4:  # read every 4th frame
            success, im = cap.retrieve()
            imgs = im if success else imgs * 0
            n = 0
            img0 = imgs.copy()

            # Letterbox
            img = [letterbox(x, imgsz, stride=stride)[0] for x in img0]

            # Stack
            img = np.stack(img, 0)

            # Convert
            # img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to bsx3x416x416
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416 
            img = np.ascontiguousarray(img) 

            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
                
            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=False)[0]
            
            # Apply NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes=[], agnostic=False)
            t2 = time_synchronized()
            
            # Process detections
            for i, det in enumerate(pred):  # detections per image
                s, im0 = '%g: ' % i, img0.copy()
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                    
                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh)  # label format

                        # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

                # Print time (inference + NMS)
                print(f'{s}Done. ({t2 - t1:.3f}s)')
                
                # Stream results
                if view_img:
                    # Display the resulting frame
                    cv2.imshow('frame',im0)
        time.sleep(1 / fps)  # wait time

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
