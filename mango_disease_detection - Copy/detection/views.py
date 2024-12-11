# from django.shortcuts import render, redirect
# import os
# from .forms import ImageUploadForm
# from .utils import predict_disease

# def classify_leaf(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             image_path = f"media/{image.name}"
            
#             # Save the uploaded image
#             with open(image_path, 'wb+') as destination:
#                 for chunk in image.chunks():
#                     destination.write(chunk)
            
#             # Predict the disease
#             result = predict_disease(image_path)
            
#             # Clean up the saved image
#             os.remove(image_path)
            
#             # Redirect to the result page with the prediction as a parameter
#             return redirect('result', prediction=result)
#     else:
#         form = ImageUploadForm()

#     return render(request, 'classify.html', {'form': form})

# def result(request, prediction):
#     return render(request, 'result.html', {'result': prediction})

from django.shortcuts import render, redirect
import os
from .forms import ImageUploadForm
from .utils import predict_disease
from django.conf import settings



# A dictionary mapping the disease names to explanations
# Updated dictionary with treatment recommendations
disease_explanations = {
    "Anthracnose": {
        "explanation": "Anthracnose is a fungal disease that affects the fruit, causing black spots and lesions.",
        "treatment": "Prune infected branches and apply a fungicide containing copper or mancozeb during the flowering stage."
    },
    "Bacterial Canker": {
        "explanation": "Bacterial Canker causes leaf drop, lesions on the bark, and dieback of twigs.",
        "treatment": "Apply copper-based bactericides and ensure proper pruning to improve air circulation."
    },
    "Cutting Weevil": {
        "explanation": "The Cutting Weevil causes damage to young mango trees by feeding on leaves and stems.",
        "treatment": "Handpick the weevils and apply neem oil or insecticides approved for mango trees."
    },
    "Die Back": {
        "explanation": "Die Back disease results in the death of branches and leaves due to fungal infection.",
        "treatment": "Prune infected branches and apply systemic fungicides to prevent further spread."
    },
    "Gall Midge": {
        "explanation": "Gall Midge causes distorted leaves and reduced growth due to larvae feeding inside plant tissue.",
        "treatment": "Use insecticides such as chlorpyrifos or acephate to control the larvae."
    },
    "Healthy": {
        "explanation": "The tree is healthy with no visible disease symptoms.",
        "treatment": "No treatment is necessary. Ensure proper watering, fertilization, and pest management."
    },
    "Powdery Mildew": {
        "explanation": "Powdery Mildew is a fungal disease that produces white, powdery patches on leaves and stems.",
        "treatment": "Apply sulfur-based fungicides or potassium bicarbonate to affected areas."
    },
    "Sooty Mould": {
        "explanation": "Sooty Mould is a fungal growth that appears as black soot on leaves, often due to insect secretion.",
        "treatment": "Control the insects (such as aphids or whiteflies) with insecticides and wash off the mould with water."
    }
}


def classify_leaf(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name.replace(" ", "_"))
            
            # Save the uploaded image
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # Predict the disease
            result = predict_disease(image_path)
            
            # Clean up the saved image after prediction
            os.remove(image_path)
            
            # Split result to get disease name and confidence
            disease_name, confidence = result.split(', ')
            disease_name = disease_name.split(': ')[1]
            confidence = confidence.split(': ')[1]
            
            # Get disease explanation and treatment
            disease_info = disease_explanations.get(disease_name, {
                "explanation": "No explanation available.",
                "treatment": "No treatment available."
            })
            
            # Pass the image path, prediction, explanation, and treatment to the result page
            return render(request, 'result.html', {
                'image_path': os.path.join(settings.MEDIA_URL, image.name),
                'predicted_disease': disease_name,
                'confidence': confidence,
                'disease_explanation': disease_info["explanation"],
                'treatment_recommendation': disease_info["treatment"]
            })
    else:
        form = ImageUploadForm()

    return render(request, 'classify.html', {'form': form})


def result(request):
    return render(request, 'result.html', {'result': prediction})
