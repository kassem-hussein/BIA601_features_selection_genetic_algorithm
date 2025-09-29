'''
FLASK APP 
'''
from genetic_algorithm import  GeneticAlgorithm
from traditional_algorithm import TraditionalAlgorithm
from flask import Flask,render_template,redirect,request,session,get_flashed_messages,flash
import pandas as pd
import time

app = Flask(__name__)
app.secret_key = "python_flask_genetic_algorithm_app"
@app.route('/')
def home():
      errors = get_flashed_messages(category_filter=['errors'])
      if len(errors) > 0:
            errors = errors[0]
      else:
            erorrs = {} 
      return  render_template('home.html',errors=errors)

@app.route('/result',methods=['POST'])
def result():
      csv_file = request.files['data']
      target   = request.form.get('target')
      compare  = request.form.get('compare')
      model_type = request.form.get('model')
      n_generations = request.form.get('n_generations')
      n_populations = request.form.get('n_populations')
      # Make vaidation on input data
      errors = {}
      if not target:
           errors.setdefault('target', []).append("target field is required")
      if type(target) != type("str"):
            errors.setdefault('target', []).append('target field must be string')
      if not n_populations:
            errors.setdefault('n_populations', []).append('Number of populations is required')
      if not model_type or model_type not in ('regression','classification'):
            errors.setdefault('model', []).append('Model type is required and should be in  (regression,classification)')

      try:
            val = int(n_populations)
            if val < 0:
                  raise ValueError
      except (TypeError, ValueError):
            errors.setdefault('n_populations',[]).append('Number of populations must be Integer and grater than 0')
      if not n_generations:
            errors.setdefault('n_generations',[]).append ('Number of generations is required')
      try:
            val = int(n_generations)
            if  val < 0:
                  raise ValueError
      except (TypeError, ValueError):
            errors.setdefault('n_generations',[]).append('Number of generations must be Integer and grater than 0')
      
      if not csv_file or  not csv_file.filename.lower().endswith('.csv'):
            errors.setdefault('data',[]).append('Data file required and must be csv file')
      
      if len(errors.keys()) > 0:
            flash(errors,'errors')
            return redirect('/#get-started')

      df = pd.read_csv(csv_file)
      if target not in df.columns:
            errors.setdefault('target', []).append('target field must be exits in data')
      if len(errors.keys()) > 0:
            flash(errors,'errors')
            return redirect('/#get-started')

      # prepare data

      df = df.select_dtypes(['number'])
      df = df.dropna()
      X =  df.drop(columns=[target])
      Y = df[target]
      start_time = time.time()
      selected_features,fitness_value,accuracy,n_selected,n_total,genrations =  GeneticAlgorithm(df, target, X, Y,model_type=model_type).start()
      end_time = time.time()
      t_accuracy = 0
      t_selected = tuple()
      t_start_time = time.time()
      if compare == "1":
            t_accuracy,t_selected  = TraditionalAlgorithm(df, X, Y, target, model_type).start()
      t_end_time= time.time()
      # display result in resutl page
      return render_template(
        'result.html',
        selected_features=selected_features,
        total_time = round(end_time - start_time,4),
        fitness=fitness_value,
        accuracy=accuracy,
        n_selected=n_selected,
        n_total=n_total,
        genrations=genrations,
        compare   = compare,
        t_selected_features =t_selected,
        t_len_selected    = len(t_selected),
        t_accuracy = t_accuracy,
        t_time    = t_end_time - t_start_time

    )

      





      



if __name__ == '__main__':
    app.run(debug=True)
