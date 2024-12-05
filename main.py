# Import necessary libraries
from flask import Flask, render_template, request  # Flask for web framework, render_template for HTML templates, request to handle form data
import pickle  # pickle to load the saved machine learning model
import numpy as np  # numpy for handling numerical data arrays

# Initialize Flask application

app = Flask(__name__)

# Load the pre-trained machine learning model from a file
with open("src/Thyroid_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Define the route for the homepage
@app.route('/')
def index():
   # Render the homepage template 'home.html'
   return render_template('home.html')

# Define the route for the 'More Information' page
@app.route("/moreinfo", methods=["GET", "POST"])
def moreinfo():
    # Render the 'moreinfo.html' template for additional information about thyroid disease
    return render_template('moreinfo.html')

# Define the route for the 'Predict' page, where users can input data
@app.route("/predict", methods=["GET", "POST"])
def predict():
    # Render the 'predict.html' template for user inputs for prediction
    return render_template('predict.html')

# Define the route for the prediction results page
@app.route("/predictresult", methods=["GET", "POST"])
def predictresult():
    # Check if the form was submitted with a POST request
    if request.method == "POST":
        # Retrieve input values from the form and convert to appropriate data types
        Age = float(request.form.get('age'))
        Sex = request.form.get('sex')
        Level_thyroid_stimulating_hormone = float(request.form.get('TSH'))
        Total_thyroxine_TT4 = float(request.form.get('TT4'))
        Free_thyroxine_index = float(request.form.get('FTI'))
        On_thyroxine = request.form.get('on_thyroxine')
        On_antithyroid_medication = request.form.get('on_antithyroid_medication')
        Goitre = request.form.get('goitre')
        Hypopituitary = request.form.get('hypopituitary')
        Psychological_symptoms = request.form.get('psych')
        T3_measured = request.form.get('T3_measured')

        # Convert categorical variables to numerical values as expected by the model
        Sex = 1 if Sex == "Male" else 0
        On_thyroxine = 1 if On_thyroxine == "True" else 0
        On_antithyroid_medication = 1 if On_antithyroid_medication == "True" else 0
        Goitre = 1 if Goitre == "True" else 0
        Hypopituitary = 1 if Hypopituitary == "True" else 0
        Psychological_symptoms = 1 if Psychological_symptoms == "True" else 0
        T3_measured = 1 if T3_measured == "True" else 0

        # Create a NumPy array with the inputs to match the model's expected input format
        arr = np.array([[Age, Sex, Level_thyroid_stimulating_hormone, Total_thyroxine_TT4,
                         Free_thyroxine_index, On_thyroxine, On_antithyroid_medication, 
                         Goitre, Hypopituitary, Psychological_symptoms, T3_measured]])

        # Use the loaded model to make a prediction
        pred = model.predict(arr)

        # Interpret the prediction result and map it to a meaningful message
        if pred == 0:
            res_Val = "Compensated Hypothyroid"
        elif pred == 1:
            res_Val = "No Thyroid"
        elif pred == 2:
            res_Val = "Primary Hypothyroid"
        elif pred == 3:
            res_Val = "Secondary Hypothyroid"

        # Format the output message with the prediction result
        Output = f"Patient has {res_Val}"

        # Render the 'predictresult.html' template with the prediction result
        return render_template('predictresult.html', output=Output)

    # If the request method is not POST, return the 'home.html' template
    return render_template("home.html")

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=False)  # Set debug to False for production
