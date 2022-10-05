from flask import Flask, render_template, request, flash, url_for, make_response
import sys
sys.path.append("venv/lib/python3.8/site-packages/pasta") #otherwise flask won't find it
import pasta_solver
#from pasta import pasta_solver
#from markupsafe import escape

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/', methods=['POST','GET']) 
def sitoHTML():
    if request.method == 'GET': #show requested page with empty form
        return render_template('sitoHTML.html')

    elif request.method == 'POST': #get the input form e give back results
        answer =''
        ProgramCode = str(request.form['inputPr'])   #1 textbox
        Query = str(request.form['inputQ'])          #2 textbox
        Evidence = str(request.form['inputEv'])           #3 textbox
        RadioButton1 = str(request.form['options'])  #one of 5 radio button
        #nSamples = request.form['options']          #nSamples
        #RadioButton2 = str(request.form['AI_options'])   #radio button for Appr Inference
        #Blocks = request.form['Blocks']                 #Blocks
        #Brave = request.form['Brave']               #brave for last 3 RButton
        
        RadioButton2=False
        if request.form.get("AI_options"):  #brave for last 3 RButton
            RadioButton2 = True


        if (not Evidence):
            Evidence = ''

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
#------------------------APPROXIMATE INFERENCE-------------------------
        elif (RadioButton1 == 'Approximate Inference'):
            if ((not Evidence) == False):
                RadioButton2 = str(request.form['AI_options'])   #radio button for Appr Inference
            else:
                RadioButton2 = None
            nSamples = request.form['options']          #nSamples

            if (not Evidence):
                solver = pasta_solver.Pasta('tmpFile.lp', Query, "", False, False, nSamples)
            else:
                solver = pasta_solver.Pasta('tmpFile.lp', Query, Evidence, False, False, nSamples)
            
            if (not RadioButton2):
                lp, up = solver.approximate_solve('approximate')
            else:
                if (RadioButton2 == 'gibbs' and (not Blocks) == False):
                    Blocks = int(request.form['Blocks'])                 #Blocks
                    lp, up = solver.approximate_solve(RadioButton2,Blocks)  
                else:
                    lp, up = solver.approximate_solve(RadioButton2) 
            answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                    '\n' + "Upper probability for the query " +  Query + ": " + str(up))
            return render_template('sitoHTML.html',CodeOut = answer)
#------------------------MAP INFERENCE-------------------------------
        elif (RadioButton1 == 'Map Inference'):
            Brave=False
            if request.form.get("Brave"):  #brave for last 3 RButton
                Brave = True
           
            solver = pasta_solver.Pasta('tmpFile.lp', Query)
            max_p, atoms_list = solver.map_inference(Brave)
            map_op = len(atoms_list) > 0 and len(atoms_list[0]) == len(solver.interface.prob_facts_dict)
            map_or_mpe = "MPE" if map_op else "MAP"
            answer = f"{map_or_mpe}: {max_p}\n{map_or_mpe} states: {len(atoms_list)}" + "\n"
            for i, el in enumerate(atoms_list):
                answer += (f"State {i}: {el}") + "\n"
            return render_template('sitoHTML.html',CodeOut = answer)
#------------------------ABDUCTION----------------------------------
        elif (RadioButton1 == 'Abduction'):
            Brave=False
            if request.form.get("Brave"):  #brave for last 3 RButton
                Brave = True
            solver = pasta_solver.Pasta('tmpFile.lp', Query)
            lp, up, abd_explanations = solver.abduction()
            abd_exp_no_dup = pasta_solver.Pasta.remove_dominated_explanations(abd_explanations)
            if len(abd_exp_no_dup) > 0 and up != 0:
                if Brave:
                    answer= f"Upper probability for the query: {up}"
                else:
                    answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                        '\n' + "Upper probability for the query " +  Query + ": " + str(up))
            n_exp = sum(1 for ex in abd_exp_no_dup if len(ex) > 0)
            answer += '\n' + f"Abductive explanations: {n_exp}"
            return render_template('sitoHTML.html',CodeOut = answer)
#------------------------PARAMETER LEARNING-------------------------
        elif (RadioButton1 == 'Parameter Learning'):
            Brave=False
            if request.form.get("Brave"):  #brave for last 3 RButton
                Brave = True


            return render_template('sitoHTML.html',CodeOut = 'answer')

        else:
            return 'SOMETHING WENT WRONG (1)'

    return 'SOMETHING WENT WRONG (2)'