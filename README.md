# Modelling Final Project Prototype
 This project focuses on developing an AI model to predict engine failures in mechanical systems. The AI model is designed to identify patterns and features that indicate imminent engine failures. The model uses a feedforward neural network (MLP) for training and GridSearchCV for hyperparameter tuning. Here are the functionalities and implementation details:

### Functionalities

1. **Model Training and Tuning**
   - The AI model is trained using a dataset with relevant engine parameters.
   - GridSearchCV is employed to fine-tune the model's hyperparameters to enhance performance.

2. **Web Application Deployment**
   - The trained model is deployed using Streamlit to create an interactive web application.
   - The web app takes inputs from the necessary features: ['engine rpm', 'lub oil pressure', 'fuel pressure', 'coolant pressure', 'lub oil temp', 'coolant temp'] from the user.
   - Based on the input features, the app predicts whether an engine is likely to fail or not, and provides the probability or likelihood of the prediction's accuracy.

### Implementation Steps

1. **Data Collection and Preparation**
   - Gather a dataset with engine parameters and their corresponding conditions.
   - Process and visualize the data to ensure it is clean and suitable for model training.

2. **Model Training**
   - Train the feedforward neural network (MLP) using the collected dataset.
   - Use GridSearchCV to tune the model's hyperparameters, such as batch size, epochs, activation functions, and learning rate.

3. **Web Application Development**
   - Develop a web application using Streamlit.
   - The app includes an interface for users to input the relevant engine parameters.
   - The app predicts the likelihood of engine failure based on the provided inputs.

4. **Running the Application**
   - To run the web application, execute the command `streamlit run app.py` in the terminal where the `app.py` script is located.

### Demonstration
Link to video: https://youtu.be/BZASjD4Dl7s
---

