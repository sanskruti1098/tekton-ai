import os, json
from flask import Flask, send_file, render_template_string, abort

PVC_PATH = os.environ.get("PVC_PATH", "/mnt/ws")
app = Flask(__name__)

TEMPLATE = '''
<html>
<head>
  <title>Heart UCI ML Metrics</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="p-4 bg-light">
  <div class="container">
    <h2 class="mb-4">Heart Disease (UCI) – ML Metrics</h2>
    {% if metrics %}
    <table class="table table-bordered table-sm">
      <thead class="table-light">
        <tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th></tr>
      </thead>
      <tbody>
      {% for model, vals in metrics.items() %}
        <tr>
          <td><b>{{ model }}</b></td>
          <td>{{ vals.accuracy|round(3) }}</td>
          <td>{{ vals.precision|round(3) }}</td>
          <td>{{ vals.recall|round(3) }}</td>
          <td>{{ vals.f1|round(3) }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="alert alert-warning">No metrics available</div>
    {% endif %}

    <h4 class="mt-5">Confusion Matrices</h4>
    <div class="row">
      <div class="col-md-6">
        <p><b>k-NN</b></p>
        <img src="/image/confusion_matrix_knn.png" class="img-fluid">
      </div>
      <div class="col-md-6">
        <p><b>MLP</b></p>
        <img src="/image/confusion_matrix_mlp.png" class="img-fluid">
      </div>
    </div>

    <a href="/metrics.json" download class="btn btn-sm btn-outline-primary mt-4">Download metrics.json</a>
  </div>
</body>
</html>
'''

def load_metrics():
    try:
        with open(os.path.join(PVC_PATH, "metrics.json")) as f:
            return json.load(f).get("all", {})
    except Exception:
        return {}

@app.route("/")
def home():
    return render_template_string(TEMPLATE, metrics=load_metrics())

@app.route("/image/<name>")
def image(name):
    path = os.path.join(PVC_PATH, name)
    if not os.path.exists(path):
        abort(404)
    return send_file(path, mimetype="image/png")

@app.route("/metrics.json")
def raw_metrics():
    return send_file(os.path.join(PVC_PATH, "metrics.json"), mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
