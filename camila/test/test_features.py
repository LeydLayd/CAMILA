import joblib
import sys

def test_feature_names():
    scaler = joblib.load("camila/models/scaler.joblib")
    
    from camila.questions.questions import preguntas_chatbot
    
    expected = list(scaler.feature_names_in_)
    actual = ["Estado", "Sexo", "Edad"] + preguntas_chatbot
    
    errores = []
    
    if len(expected) != len(actual):
        errores.append(f"❌ Longitud diferente: scaler espera {len(expected)} columnas, tienes {len(actual)}")
    
    for i, (e, a) in enumerate(zip(expected, actual)):
        if e != a:
            errores.append(f"❌ Columna {i}: scaler='{e}' | questions.py='{a}'")
    
    if errores:
        print("\n".join(errores))
        sys.exit(1)
    else:
        print(f"✅ Todas las {len(expected)} columnas coinciden perfectamente.")

def test_evaluar_relacion():
    from camila.tools.tools import evaluar_relacion

    # Simular tool_context con 33 respuestas de prueba
    class FakeToolContext:
        state = {
            "respuestas": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           0, 0, 1, 0, 1, 0, 1, 1, 0, 1,
                           1, 1, 1]
        }

    resultado = evaluar_relacion(
        estado="En una relación",
        sexo="Masculino",
        edad=22,
        tool_context=FakeToolContext()
    )

    print("\n--- Resultado evaluar_relacion ---")
    print(f"Red Neuronal:")
    print(f"  Funcionalidad:    {resultado['red_neuronal']['funcionalidad']}%")
    print(f"  Disfuncionalidad: {resultado['red_neuronal']['disfuncionalidad']}%")
    print(f"Random Forest:")
    print(f"  Funcionalidad:    {resultado['random_forest']['funcionalidad']}%")
    print(f"  Toxicidad:        {resultado['random_forest']['toxicidad']}%")

    # Validar que el resultado tiene la estructura correcta
    assert "red_neuronal" in resultado, "❌ Falta clave red_neuronal"
    assert "random_forest" in resultado, "❌ Falta clave random_forest"
    assert 0 <= resultado['red_neuronal']['funcionalidad'] <= 100, "❌ Valor fuera de rango"
    assert 0 <= resultado['random_forest']['toxicidad'] <= 100, "❌ Valor fuera de rango"
    
    print("\n✅ evaluar_relacion funciona correctamente.")

if __name__ == "__main__":
    test_feature_names()
    test_evaluar_relacion()