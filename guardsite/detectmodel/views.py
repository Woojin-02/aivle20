from django.shortcuts import render
import numpy as np
import onnxruntime as ort
from PIL import Image
# Create your views here.
def models():
    bi_path = "models/best_binary_weights.onnx"
    danger_path = "models/best_5danger.onnx"

    img_path = 'img/a.jpg'
    label_v5 = ['추락','낙하','협착','화재','전도']

    # 모델 불러오기
    bi_session = ort.InferenceSession(bi_path)
    danger_session = ort.InferenceSession(danger_path)

    # 이미지 불러오기
    img = Image.open(img_path)
    img = img.resize((640, 640))
    image_array = np.array(img, dtype=np.float32) / 255.0 
    image_array = image_array.transpose((2, 0, 1))
    image_array = np.expand_dims(image_array, axis=0)

    # 각 모델의 입력 이름 가져오기
    bi_input_name = bi_session.get_inputs()[0].name
    bi_output_name = bi_session.get_outputs()[0].name
    danger_input_name = danger_session.get_inputs()[0].name
    danger_output_name = danger_session.get_outputs()[0].name

    # 입력 데이터 준비
    bi_input_data = {bi_input_name: image_array}
    danger_input_data = {danger_input_name: image_array}

    # 이진 분류 모델 추론
    bi_output = bi_session.run([bi_output_name], bi_input_data)[0]
    bi_prediction = bi_output.squeeze(0)

    # 5가지 위험 요소 분류 모델 추론
    dan_output = danger_session.run([danger_output_name], danger_input_data)[0]
    dan_prediction = dan_output.squeeze(0)