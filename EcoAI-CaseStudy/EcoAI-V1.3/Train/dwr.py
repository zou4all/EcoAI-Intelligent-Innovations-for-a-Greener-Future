from roboflow import Roboflow
rf = Roboflow(api_key="unauthorized")
project = rf.workspace("ayush-ll9z4").project("swimming-pools-dctlb-qd7rr")
version = project.version(1)
dataset = version.download("yolov5-obb")
                