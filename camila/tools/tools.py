

def guardar_respuesta(respuesta: bool, tool_context) -> dict:
    lista = tool_context.state.get("respuestas", [])
    lista.append(1 if respuesta else 0)
    tool_context.state["respuestas"] = lista
    return {"guardado": True, "total": len(lista)}

def obtener_respuestas(tool_context) -> dict:
    lista = tool_context.state.get("respuestas", [])
    return {"respuestas": lista}

def evaluar_relacion(estado: str, sexo: str, edad: int, tool_context) -> dict:
    """
    Evalúa la relación usando Random Forest y Red Neuronal.
    Llamar al terminar las 33 preguntas.
    estado: 'En una relación'
    sexo: 'Masculino' o 'Femenino'
    edad: edad del usuario
    """
    MODEL_DIR = "camila/models"
    from camila.questions.questions import preguntas_chatbot
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    import joblib
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.optimizers import Adam

    # 1. Obtén las respuestas guardadas del tool_context
    respuestas = tool_context.state.get("respuestas", [])

    # 2. Arma el DataFrame con el orden correcto:
    # Estado, Sexo, Edad, P1...P33
    datos = {
        'Estado': [1],
        'Sexo': [1 if sexo == 'Masculino' else 0],
        'Edad': [edad],
    }
    for i, r in enumerate(respuestas):
        datos[preguntas_chatbot[i]] = [r]

    df = pd.DataFrame(datos)
    dfglogabl = pd.DataFrame(datos)

    X = df.iloc[:, :36]

    # 3. Carga los modelos desde ./models
    modelo = load_model(f'{MODEL_DIR}/modelo_red_neuronal.h5')
    scaler = joblib.load(f'{MODEL_DIR}/scaler.joblib')
    modeloR = joblib.load(f'{MODEL_DIR}/modelo_rf_multi.pkl')
    # 4. Preprocesa y predice con ambos
    X_scaled = scaler.transform(X)
    predicciones = modelo.predict(X_scaled)
    pglobal = predicciones
    probabilidad_relacion_funcional = round(predicciones[0][0] * 100, 1)
    probabilidad_relacion_disfuncional = round(predicciones[0][1] * 100, 1)

    X_rf = df.iloc[:, 3:35].copy()
    X_rf['Estado'] = df['Estado']
    X_rf['Sexo'] = df['Sexo']
    X_rf['Edad'] = df['Edad']
    predicciones = modeloR.predict_proba(X_rf)
    pglobal = predicciones
    func_percent = round(predicciones[0][0][1] * 100, 1)
    toxic_percent = round(predicciones[1][0][1] * 100, 1)
    
    return {
    "red_neuronal": {
        "funcionalidad": float(probabilidad_relacion_funcional),
        "disfuncionalidad": float(probabilidad_relacion_disfuncional)
    },
    "random_forest": {
        "funcionalidad": float(func_percent),
        "toxicidad": float(toxic_percent)
    }
}
    
    