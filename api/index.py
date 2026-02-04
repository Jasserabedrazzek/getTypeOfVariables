import ast
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

def analyze_python_code(code_string):
    try:
        tree = ast.parse(code_string)
        variables = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        var_value = "Expression complexe"
                        var_type = "Inconnu"

                        value_node = node.value

                        if isinstance(value_node, ast.Constant):
                            var_value = value_node.value
                            var_type = type(value_node.value).__name__
                        
                        elif isinstance(value_node, ast.Call):
                            if hasattr(value_node.func, 'id'):
                                var_value = f"Résultat de {value_node.func.id}()"
                            var_type = "Fonction"

                        elif isinstance(value_node, ast.List):
                            var_value = "Liste [...]"
                            var_type = "list"

                        variables.append({
                            "name": var_name,
                            "value": str(var_value),
                            "type": var_type
                        })
        return {"success": True, "variables": variables}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data or 'code' not in data:
        return jsonify({"error": "Aucun code fourni"}), 400
    
    result = analyze_python_code(data['code'])
    return jsonify(result)

@app.route('/')
def home():
    return "API d'analyse Python en ligne !"

# IMPORTANT : Pas de app.run() pour Vercel
