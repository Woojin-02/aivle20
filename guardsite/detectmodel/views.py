from django.shortcuts import render, redirect,get_object_or_404,reverse
from .forms import DangerForm
from .models import DangerModel
import numpy as np
import onnxruntime as ort
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def models(image):
    bi_path = "models/best_binary_9.onnx"
    danger_path = "models/best_5danger.onnx"
    
    label_v5 = ['Fall','Drop','Crash','Fire','Overthrow']
    # 모델 불러오기
    bi_session = ort.InferenceSession(bi_path)
    danger_session = ort.InferenceSession(danger_path)
    # 이미지 불러오기
    image = Image.open(image)
    image = image.resize((640, 640))
    image_array = np.array(image, dtype=np.float32) / 255.0 
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
    # 5가지 위험 요소 분류 모델 추론
    
    if(np.argmax(bi_output)):
        dan_output = danger_session.run([danger_output_name], danger_input_data)[0]
        print(dan_output)
        return label_v5[np.argmax(dan_output)]
    else:
        return 'Safe'
    


# 이미지 업로드 및 결과 표시 뷰
    
@login_required
def danger_post(request):
    if request.method == 'POST':
        form = DangerForm(request.POST, request.FILES)
        
        if form.is_valid():
            danger_form = form.save(commit=False)
            predictions = models(danger_form.image)
            danger_form = DangerModel(
                image=danger_form.image,
                danger=predictions,
                area=danger_form.area
            )
            context = {'images': danger_form.image,
                       'danger': predictions, 
                       'area':danger_form.area}
            
            danger_form.save()
            return render(request, 'detectmodel/checked.html', context)
    else:
        form = DangerForm()
    return render(request, 'detectmodel/index.html', {'form': form})


def index(request):
    dangers = DangerModel.objects.all()
    page = request.GET.get("page",1)
    paginator = Paginator(dangers,6)
    object_list = paginator.get_page(page)
    
    
    context = {
        'dangers':object_list
    }
    return render(request,'detectmodel/index.html',context)


def detail(request,danger_pk):
    danger = get_object_or_404(DangerModel,pk=danger_pk)
    
    context = {
        'danger':danger,
    }
    return render(request,'detectmodel/detail.html',context)
    