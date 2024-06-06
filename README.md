# Sensor Teaching - Backend

This app provides a real-time dashboard for teachers to obtain a better overview of students in a class. The system works by continuously measuring physiological data from smart wristbands and web cameras and displaying relevant information visually on the dashboard. This is the frontend part of the application and contains a dashboard created in React using Typescript. To use the full application, the backend needs to run as well. This system is currently configured to use Firebase Realtime Database. Other databases can be used, but this requires modifications of the code to ensure compatibility with the chosen database technology.

The Frontend and Backend works independently, meaning that they can both run separately without the other part. This is because data from the backend(s) are sent to the database, and the frontend fetches data from the database. If only backend(s) are running, data will be gathered to the database, but not shown in the dashboard. If only the frontend is running, old or no data will be shown on the dashboard. It should still run the frontend for debugging or testing purposes.

## Getting started

The system uses a PCs web camera along with [Empatica E4 wristbands](https://www.empatica.com/store/e4-wristband/) to capture students' physiological states. Therefore, a web camera is required on each PC running the backend, along with enough wristbands to cover all students which will use the system.

### Required software

- Python
- Django
- Empatica BLE Server

### Configuration and setup

The following steps has to be done for each PC going to run the backend. The code is captured to monitor two students at a time, so to monitor 10 students in total, this backend has to be runned on 5 PCs.

 1. Clone the repository to your local machine:  `git clone https://github.com/hakonbjork/master-backend.git` (kanskje endre)
 2. Navigate to the project folder
 3. Install the required packages using `pip` or `conda`: `django`, `djangorestframework`, `djang-cors-headers`, `firebase-admin`, `opencv-python`, `PyEmotion`, `statsmodels`
 4. In order to obtain changes we made to the PyEmotion package, the `main.py` file of the framework has to be replaced with the code below. Eventually, only the `predict_emotion()` function can be replaced as this is the only one which is changed.
    <details>
    <summary><b>Main.py in PyEmotion</b></summary>
      
    ```python
    from .networks import NetworkV2
    import torch
    import torchvision.transforms as transforms
    import numpy as np
    import cv2 as cv
    from facenet_pytorch import MTCNN
    import os
    from art import *
    from termcolor import colored, cprint
    
    def PyEmotion():
      text = colored(text2art("PyEmotion"), 'magenta')
      print(text)
      print(colored('Welcome to PyEmotion ', 'magenta'))
    
    
    class DetectFace(object):
      def __init__(self, device, gpu_id=0):
        assert device == 'cpu' or device == 'gpu'
        if torch.cuda.is_available():
          if device == 'cpu':
            print('[*]Warning: Your device have GPU, for better performance do EmotionRecognition(device=gpu)')
            self.device = torch.device('cpu')
          if device == 'gpu':
            self.device = torch.device(f'cuda:{str(gpu_id)}')
        else:
          if device == 'gpu':
            print('[*]Warning: No GPU is detected, so cpu is selected as device')
            self.device = torch.device('cpu')
          if device == 'cpu':
            self.device = torch.device('cpu')
    
        self.network = NetworkV2(in_c=1, nl=32, out_f=7).to(self.device)
        self.transform = transforms.Compose([
          transforms.ToPILImage(),
          transforms.Resize((48, 48)),
          transforms.ToTensor(),
          transforms.Normalize(mean=[0.5], std=[0.5])
        ])
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        model_dict = torch.load(os.path.join(os.path.dirname(__file__), 'model', 'main_model.pkl'), map_location=torch.device(self.device))
        self.emotions = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
        self.network.load_state_dict(model_dict['network'])
        self.network.eval()
    
      def _predict(self, image):
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        output = self.network(tensor)
        ps = torch.exp(output).tolist()
        index = np.argmax(ps)
        return self.emotions[index]
    
      def predict_emotion(self, frame):
        f_h, f_w, c = frame.shape
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        boxes, _ = self.mtcnn.detect(frame)
        emotions = [] # addded
        if boxes is not None:
          boxes = sorted(boxes, key=lambda box: -box[0]) # added
          for i in range(len(boxes)):
            x1, y1, x2, y2 = int(round(boxes[i][0])), int(round(boxes[i][1])), int(round(boxes[i][2])), int(round(boxes[i][3]))
            emotion = self._predict(gray[y1:y2, x1:x2])
            emotions.append(emotion) # added
            frame = cv.rectangle(frame, (x1, y1), (x2, y2), color=[255, 0, 137], thickness=2)
            frame = cv.rectangle(frame, (x1, y1 - int(f_h*0.03125)), (x1 + int(f_w*0.125), y1), color=[255, 0, 137], thickness=-1)
            frame = cv.putText(frame, text=emotion, org=(x1 + 5, y1 - 3), fontFace=cv.FONT_HERSHEY_PLAIN, color=[255, 255, 255], fontScale=1, thickness=1)
          return frame, emotions # modified
        else:
          emotion = 'NoFace'
          return frame, [emotion] # modified
    ```
    
    </details>
 5. Install Empatica BLE Server as specified on their [website](https://developer.empatica.com/windows-streaming-server-usage.html)
    - As specified on the website, a [Bluegiga Bluetooth Smart Dongle](https://www.silabs.com/wireless/bluetooth/bluegiga-low-energy-legacy-modules/device.bled112?tab=specs)         is required in order for the streaming server to connect to Empatica E4 wristbands
 6. Create an id for each student/user of the system. This can be a string of your choice, the only requirement is that each ID is unique
 7. Change the mapping in `init_empatica.py` to match your chosen ids with one Empatica E4 each. The Empatica E4 is the ID that can be seen in the streaming server, after          "E4_". An example of the mapping can be seen below:
    <details>
    <summary><b>Mapping Example</b></summary>
      
    ```python
    id_mapping = {
          "H1": "904ACD",
          "H2": "D631CD",
          "I1": "414D5C",
          "I2": "A333CD",
          "L1": "C13A64",
          "L2": "322C64",
      }
    ```
    
    </details>

  10. Create an empty 'data' folder in the root level of the repository. This folder will contain the ids for the PC in use.

### Running the Backend

  1. Run the backend using `python manage.py runserver --noreload`
  2. Navigate to [localhost:8000](http://localhost:8000/) on the PC to specify the ids that PC will use. This is equivalent to the ids of the two students working on that PC
  3. After the form containing ids are sent in, the system will begin gathering data and sending information to the database.

## Authors

Further questions about the system can be directed to the authors of the project via mail:
- cecilikn@stud.ntnu.no
- haakofb@stud.ntnu.no
