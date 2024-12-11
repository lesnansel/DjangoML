from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# Path to the model file
MODEL_PATH = 'detection/models/MangoCare.h5'

# Load the trained model
model = load_model(MODEL_PATH)

# Print the model's input shape to verify
print(model.summary())
print("Model input shape:", model.input_shape)
# Print the full prediction output (probabilities for all classes)
# print("Prediction probabilities:", prediction)


# Function to predict disease from an image
def predict_disease(image_path):
    # Check if the file exists before proceeding
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image at {image_path} was not found.")

    # Load and preprocess the image
    try:
        # Resize the image to the expected input size (150x150) and convert it to an array
        img = image.load_img(image_path, target_size=(150, 150))  
        img_array = image.img_to_array(img)  # Convert to a NumPy array
        img_array = img_array / 255.0  # Normalize the image to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    except Exception as e:
        raise ValueError(f"Error while processing the image: {e}")

    # Check if the shape of the image is correct
    print("Processed image shape:", img_array.shape)  # Should print (1, 150, 150, 3)
    print("Pixel value range:", img_array.min(), "to", img_array.max())

    # Predict the class
    try:
        prediction = model.predict(img_array)
    except Exception as e:
        raise ValueError(f"Error during model prediction: {e}")

    # Get the predicted class index (the class with the highest probability)
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = prediction[0][predicted_class] * 100  # Confidence of the top prediction

    # Map class indices to disease names
    class_labels = {
        0: "Anthracnose",
        1: "Bacterial Canker",
        2: "Cutting Weevil",
        3: "Die Back",
        4: "Gall Midge",
        5: "Healthy",
        6: "Powdery Mildew",
        7: "Sooty Mould",
        8: "Unhealthy",
    }

    # Get the disease name based on the predicted class
    disease_name = class_labels.get(predicted_class, "Unknown disease")

    return f"Predicted Disease: {disease_name}, Confidence: {confidence:.2f}%"

# Example usage
if __name__ == "__main__":
    # Path to the test image
    test_image_path = 'th (2).jpg'

    # Predict and print the result
    try:
        result = predict_disease(test_image_path)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
