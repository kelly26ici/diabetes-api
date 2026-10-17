# Diabetes API — ML Inference Service

A FastAPI inference service that serves a trained scikit-learn classifier for predicting diabetes risk from the standard Pima Indians Diabetes feature set. The model is serialised with `pickle` and loaded once at startup; prediction is a single synchronous endpoint with Pydantic-validated input.

---

## Endpoint

### `POST /diabetes_prediction`

Classify a patient record as diabetic or not.

**Request body**

```json
{
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}
```

**Response**

```json
{
  "prediction": 1,
  "result": "Diabetic"
}
```

`prediction` is the raw class label (`1` = diabetic, `0` = not); `result` is the human-readable string.

All eight fields are required. `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin` and `Age` are integers; `BMI` and `DiabetesPedigreeFunction` are floats. Invalid or missing fields are rejected by Pydantic before reaching the model, with a `422` response.

---

## Feature reference

| Field | Type | Meaning |
| :--- | :--- | :--- |
| `Pregnancies` | int | Number of pregnancies |
| `Glucose` | int | Plasma glucose concentration (oral glucose tolerance test) |
| `BloodPressure` | int | Diastolic blood pressure (mm Hg) |
| `SkinThickness` | int | Triceps skinfold thickness (mm) |
| `Insulin` | int | 2-hour serum insulin (mu U/ml) |
| `BMI` | float | Body mass index (kg/m²) |
| `DiabetesPedigreeFunction` | float | diabetes pedigree function (genetic risk score) |
| `Age` | int | Age in years |

---

## Running

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Interactive API docs are available at `http://localhost:8000/docs` once running.

### Docker

```bash
docker build -t diabetes-api .
docker run -p 8000:8000 diabetes-api
```

---

## Layout

```text
main.py               FastAPI app, ModelInput schema, /diabetes_prediction endpoint
diabetes_app.py       Model training / experimentation script
diabetes_model.pkl    Trained scikit-learn classifier (loaded at import time)
requirements.txt      Runtime dependencies
```

---

## Notes

- The model file is loaded at module import, so the first request pays no deserialisation cost — subsequent predictions are pure inference.
- This is an inference service, not a clinical device. Output is a model prediction on historical survey data and is not a medical diagnosis.

## License

MIT — see [LICENSE](LICENSE).
