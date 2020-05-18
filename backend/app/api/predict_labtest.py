from app import db, app
from flask import jsonify, request, url_for, g, abort
from app.api import bp
from app.models import Attendance
from app.api.errors import bad_request
from app.api.auth import token_auth
#Models
from app.ai_models.covid19_predictor import labtest_predictor


@bp.route('/predict_labtest/<int:id>', methods=['GET'])
@token_auth.login_required
def predict_labtest(id):
    """
    Return all informations about the user currently logged in
    """
    null = None #if return some null
    patient_dict = Attendance.query.get_or_404(id).to_dict()
    
    patient_cbc_predictor = labtest_predictor(patient_dict) 
    cbc_to_model = patient_cbc_predictor.preprocessing() 
    patient_prediction = patient_cbc_predictor.predict(cbc_to_model) 


    pred = patient_prediction['pred_class']
    prob = patient_prediction['pred_proba']
    
    patient_interpretation = patient_cbc_predictor.model_interpretation(patient_dict['id'], 
                                                                        cbc_to_model, 
                                                                        pred, 
                                                                        prob, 
                                                                        patient_cbc_predictor.classifier)


    return jsonify(patient_interpretation)

