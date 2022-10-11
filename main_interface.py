from flask import Flask, render_template, request, flash, url_for, make_response
import sys
sys.path.append("venv/lib/python3.8/site-packages/pasta") #otherwise flask won't find it
import pasta_solver

#####################################################################
#                workaround for printing results                    #
#####################################################################
from io import StringIO 
import sys

class Capturing(list):                    #associate print() to a list
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def external_method():              #redirecting pasta lib stdout
  print ("print something out, don't return")

class MyBuffer(object):
  def __init__(self):
    self.buffer = []
  def write(self, *args, **kwargs):
    self.buffer.append(args)

import sys
old_stdout = sys.stdout
sys.stdout = MyBuffer()
external_method()
my_buffer, sys.stdout = sys.stdout, old_stdout
print (my_buffer.buffer)
#####################################################################
#                workaround for printing results                    #
#####################################################################


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/', methods=['POST','GET']) 
def sitoHTML():
    if request.method == 'GET': #show requested page with empty form
        return render_template('sitoHTML.html')

    elif request.method == 'POST': #get the input form and give back results
        answer =''
        ProgramCode = str(request.form['inputPr'])   #1 textbox
        Query = str(request.form['inputQ'])          #2 textbox
        Evidence = str(request.form['inputEv'])           #3 textbox
        RadioButton1 = str(request.form['options'])  #one of 5 radio button
        #nSamples = request.form['options']          #nSamples
        #RadioButton2 = str(request.form['AI_options'])   #radio buttons for Appr Inference
        #Blocks = request.form['Blocks']                 #Blocks
        #Upper = request.form['Upper']               #upper for last 3 RButton
        
        #RadioButton2=False
        #if request.form.get("AI_options"):
        #    RadioButton2 = True

        #if (not Evidence): #in teoria non funziona
        #    Evidence = ''

        if (not RadioButton1):
            flash('SELECT ONE OPTIONS!') #porbably not needed - handled by HTML page
        if (not Query and RadioButton1!='Parameter Learning'):
            flash('QUERY MUST BE FILLED')


        """ Sending the program as a string might cause some issues
            as line break on the form cause some sort of errors 
            with pasta module. This is why a temporary file is
            created to get around this issue. The file is overwritten
            with any new POST call.
        """
        tmpFile = open('tmpFile.lp','w') 
        tmpFile.write(ProgramCode)
        tmpFile.close()
        
#------------------------EXACT INFERENCE------------------------------
        if (RadioButton1 == 'Exact Inference'):
            if (not Evidence):
                solver = pasta_solver.Pasta('tmpFile.lp', Query)
            else:
                solver = pasta_solver.Pasta('tmpFile.lp', Query, Evidence)
            
            lp, up = solver.inference()      
            answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                    '\n' + "Upper probability for the query " +  Query + ": " + str(up))
            return render_template('sitoHTML.html',CodeOut = answer)

#------------------------APPROXIMATE INFERENCE------------------------
        elif (RadioButton1 == 'Approximate Inference'):

            if ((not Evidence) == False): 
                Evidence = ''                      #per evitare che vengano richiesti se manca l'Evidence
                RadioButton2 = str(request.form['AI_options'])  #radio button for Appr Inference
            else:
                RadioButton2 = None
            nSamples = request.form['options']                  #nSamples

            solver = pasta_solver.Pasta('tmpFile.lp', Query, Evidence)
            
            if (not RadioButton2):
                lp, up = solver.approximate_solve()
            else:
                if (True):
                    lp, up = solver.approximate_solve()
                    
                #elif (RadioButton2 == 'gibbs' and (not Blocks) == False):
                #    Blocks = int(request.form['Blocks'])                 #Blocks
                #    lp, up = solver.approximate_solve(RadioButton2,Blocks)  
                #else:
                #    lp, up = solver.approximate_solve(RadioButton2) 
            answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                    '\n' + "Upper probability for the query " +  Query + ": " + str(up))
            return render_template('sitoHTML.html',CodeOut = answer)

#------------------------MAP INFERENCE-------------------------------
        elif (RadioButton1 == 'Map Inference'):
            solver = pasta_solver.Pasta('tmpFile.lp', Query)
            
            if request.form.get("Upper"):  #upper for last 3 Button
                #Upper = True
                max_p, atoms_list = solver.upper_mpe_inference() #may cause 'EMPY_RESPONSE' error if not used properly
            else:
                #Upper=False
                max_p, atoms_list = solver.map_inference()

            map_op = len(atoms_list) > 0 and len(atoms_list[0]) == len(solver.interface.prob_facts_dict)
            map_or_mpe = "MPE" if map_op else "MAP"
            answer = f"{map_or_mpe}: {max_p}\n{map_or_mpe} states: {len(atoms_list)}" + "\n"
            for i, el in enumerate(atoms_list):
                answer += (f"State {i}: {el}") + "\n"
            return render_template('sitoHTML.html',CodeOut = answer)

#------------------------ABDUCTION----------------------------------
        elif (RadioButton1 == 'Abduction'):
            
            solver = pasta_solver.Pasta('tmpFile.lp', Query)

            if request.form.get("Upper"):  #upper for last 3 Button
                Upper = True
            else:
                Upper=False
                
            lp, up, abd_explanations = solver.abduction()

            abd_exp_no_dup = pasta_solver.Pasta.remove_dominated_explanations(abd_explanations)
            if len(abd_exp_no_dup) > 0 and up != 0:
                if Upper:
                    answer= f"Upper probability for the query: {up}"
                else:
                    answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                        '\n' + "Upper probability for the query " +  Query + ": " + str(up))
            n_exp = sum(1 for ex in abd_exp_no_dup if len(ex) > 0)
            answer += '\n' + f"Abductive explanations: {n_exp}"
            return render_template('sitoHTML.html',CodeOut = answer)

#------------------------PARAMETER LEARNING-------------------------
        elif (RadioButton1 == 'Parameter Learning'):
            solver = pasta_solver.Pasta('tmpFile.lp', Query)

            if request.form.get("Upper"):  #upper for last 3 Button
                Upper = True
            else:
                Upper=False

            with Capturing() as answer:
                    solver.parameter_learning(Upper)

            return render_template('sitoHTML.html',CodeOut = answer)

        else:
            return 'SOMETHING WENT WRONG: ERROR CODE(1)'

    return 'SOMETHING WENT WRONG: ERROR CODE(2)'