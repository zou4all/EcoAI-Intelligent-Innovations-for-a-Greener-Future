
### **size of the data**:
Train : 24 image
validation : 5 image 

### **Best Results Achieved with YOLOv5**

| **Metric**         | **Value**          |
|---------------------|--------------------|
| **Precision**       | **93.65%**         |
| **Recall**          | **98.74%**         |
| **mAP@50**          | **97.80%**         |
| **mAP@50-95**       | **43.00%**         |


### Train :
The best results were achieved using the following execution command:

 ```
python train.py --img 640 --batch 16 --epochs 300 --data pool_dataset.yaml --weights yolov5m.pt --hyp hyp.scratch-med.yaml                                                                                             
```