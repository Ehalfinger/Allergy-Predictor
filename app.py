from flask import Flask, request, render_template 
import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn')

app = Flask(__name__)

@app.route('/')
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/allergyPredictor')
def allergyPredictor():
    return render_template("allergyPredictor.html")

def preprocessDataAndPredict(hltprnt, chldhhe, hltprbn, domicil, hltprsc, alcbnge, cgtsmok, alcfreq,
                             dshltms, dosprt, health, fnsdfml, hltprbp, eatveg, rlgdgr, hltprhb, happy):
    # Create DataFrame from inputs
    data = pd.DataFrame({
        'hltprnt': [hltprnt],
        'chldhhe': [chldhhe],
        'hltprbn': [hltprbn],
        'domicil': [domicil],
        'hltprsc': [hltprsc],
        'alcbnge': [alcbnge],
        'cgtsmok': [cgtsmok],
        'alcfreq': [alcfreq],
        'dshltms': [dshltms],
        'dosprt': [dosprt],
        'health': [health],
        'fnsdfml': [fnsdfml],
        'hltprbp': [hltprbp],
        'eatveg': [eatveg],
        'rlgdgr': [rlgdgr],
        'hltprhb': [hltprhb],
        'happy': [happy]
    })

    file = open("allergy_model.pkl", "rb")
    model_data = joblib.load(file)
    file.close()

    # Extract model and threshold
    trained_model = model_data['model']
    best_threshold = model_data['best_threshold']

    # Use the model to predict probabilities
    proba = trained_model.predict_proba(data)[0][1]

    # Apply threshold to determine the prediction
    prediction = 1 if proba >= best_threshold else 0

    return np.round(proba * 100, 1).tolist()

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        try:
            # Collect form data
            form_data = {key: request.form.get(key) for key in request.form.keys()}
            print("Form Data Received:", form_data)  # Log received data for debugging
            
            # Convert inputs to integers
            hltprnt = int(form_data['hltprnt'])
            chldhhe = int(form_data['chldhhe'])
            hltprbn = int(form_data['hltprbn'])
            domicil = int(form_data['domicil'])
            hltprsc = int(form_data['hltprsc'])
            alcbnge = int(form_data['alcbnge'])
            cgtsmok = int(form_data['cgtsmok'])
            alcfreq = int(form_data['alcfreq'])
            dshltms = int(form_data['dshltms'])
            dosprt = int(form_data['dosprt'])
            health = int(form_data['health'])
            fnsdfml = int(form_data['fnsdfml'])
            hltprbp = int(form_data['hltprbp'])
            eatveg = int(form_data['eatveg'])
            rlgdgr = int(form_data['rlgdgr'])
            hltprhb = int(form_data['hltprhb'])
            happy = int(form_data['happy'])

            # Call prediction function
            prediction = preprocessDataAndPredict(hltprnt, chldhhe, hltprbn, domicil, hltprsc, 
                                                  alcbnge, cgtsmok, alcfreq, dshltms, dosprt, 
                                                  health, fnsdfml, hltprbp, eatveg, rlgdgr, 
                                                  hltprhb, happy)

            # Return prediction to the template
            return render_template('predict.html', prediction=prediction)

        except ValueError as ve:
            print("ValueError:", str(ve))
            return render_template('predict.html', message="Please enter valid numerical values for all fields.")

        except Exception as e:
            print("General Error:", str(e))
            return render_template('predict.html', message=f"An unexpected error occurred: {str(e)}")

    # Render predict page if method is GET
    return render_template('predict.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

# Run on the correct port
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080, debug=True)