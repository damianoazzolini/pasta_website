from flask import render_template, request, flash, Blueprint, url_for, make_response
import sys
sys.path.append("venv/lib/python3.8/site-packages/pasta") #otherwise flask won't find it
import pasta_solver
from flaskr.__init__ import *

#####################################################################
#      workaround for printing results on Parameter Learning        #
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
    print ("")

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
#      workaround for printing results on Parameter Learning        #
#####################################################################

class arguments: #for approximate inference
    rejection : bool
    mh : bool
    gibbs : bool
    block : int

bp = Blueprint('main_interface', __name__, url_prefix='/')

@bp.route("/", methods=["POST","GET"]) 
def sitoHTML():
    if request.method == "GET": #show requested page with empty form
        return render_template("sitoHTML.html")

    elif request.method == "POST": #get the input form and give back results
        answer =""
        ProgramCode = str(request.form["inputPr"])   #1 textbox
        Query = str(request.form["inputQ"])          #2 textbox
        Evidence = str(request.form["inputEv"])           #3 textbox
        RadioButton1 = str(request.form["options"])  #one of 5 radio button

        if (not RadioButton1):
            flash("SELECT ONE OPTIONS!") #porbably not needed - handled by HTML page
        if (not Query and RadioButton1!="Parameter Learning"):
            flash("QUERY MUST BE FILLED")


        """ Sending the program as a string might cause some issues
            as line break on the form cause some sort of errors 
            with pasta module. This is why a temporary file is
            created to get around this issue. The file is overwritten
            with any new POST call.
        """
        tmpFile = open("tmpFile.lp","w") 
        tmpFile.write(ProgramCode)
        tmpFile.close()
        
        #####################################################################
        #                           EXACT INFERENCE                         #
        #####################################################################
        if (RadioButton1 == "Exact Inference"):
            if (not Evidence):
                solver = pasta_solver.Pasta("tmpFile.lp", Query)
            else:
                solver = pasta_solver.Pasta("tmpFile.lp", Query, Evidence)
            
            lp, up = solver.inference()      
            answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                    "\n" + "Upper probability for the query " +  Query + ": " + str(up))
            return render_template("sitoHTML.html",CodeOut = answer)

        #####################################################################
        #                        APPROXIMATE INFERENCE                      #
        #####################################################################
        elif (RadioButton1 == "Approximate Inference"):
            args = arguments
            nSamples = int(request.form["nSamples"])                  #nSamples

            if (not Evidence):
                Evidence = ""
                args.rejection  = False
                args.mh         = False
                args.gibbs      = False
                args.block      = 0
            else:
                RadioButton2 = str(request.form["AI_options"])  #radio button for Appr Inference        
                if (RadioButton2 == "gibbs"):
                    Blocks_string = str(request.form["Blocks"])
                    args.rejection  = False
                    args.mh         = False
                    args.gibbs      = True
                    args.block      = 0
                    if ((not Blocks_string) == False):
                        Blocks = int(Blocks_string)
                        args.block  = Blocks
                elif (RadioButton2 == "mh"):
                    args.rejection  = False
                    args.mh         = True
                    args.gibbs      = False
                    args.block      = 0
                elif (RadioButton2 == "rejection"):
                    args.rejection  = True
                    args.mh         = False
                    args.gibbs      = False
                    args.block      = 0
                else:
                    answer = "ERRORR - approximate inference"

            solver = pasta_solver.Pasta("tmpFile.lp", Query, Evidence, False, False, nSamples)
            lp, up = solver.approximate_solve(args)
            answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                    "\n" + "Upper probability for the query " +  Query + ": " + str(up))
            return render_template("sitoHTML.html",CodeOut = answer)

        #####################################################################
        #                           MAP INFERENCE                           #
        #####################################################################
        elif (RadioButton1 == "Map Inference"):
            solver = pasta_solver.Pasta("tmpFile.lp", Query)
            
            if request.form.get("Upper"):  #upper for last 3 Button
                #Upper = True
                max_p, atoms_list = solver.upper_mpe_inference()
            else:
                #Upper=False
                max_p, atoms_list = solver.map_inference()

            map_op = len(atoms_list) > 0 and len(atoms_list[0]) == len(solver.interface.prob_facts_dict)
            map_or_mpe = "MPE" if map_op else "MAP"
            answer = f"{map_or_mpe}: {max_p}\n{map_or_mpe} states: {len(atoms_list)}" + "\n"
            for i, el in enumerate(atoms_list):
                answer += (f"State {i}: {el}") + "\n"

            return render_template("sitoHTML.html",CodeOut = answer)

        #####################################################################
        #                               ABDUCTION                           #
        #####################################################################
        elif (RadioButton1 == "Abduction"):
            
            solver = pasta_solver.Pasta("tmpFile.lp", Query)

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
                        "\n" + "Upper probability for the query " +  Query + ": " + str(up))
            n_exp = sum(1 for ex in abd_exp_no_dup if len(ex) > 0)
            answer += "\n" + f"Abductive explanations: {n_exp}"
            
            return render_template("sitoHTML.html",CodeOut = answer)

        #####################################################################
        #                         PARAMETER LEARNING                        #
        #####################################################################
        elif (RadioButton1 == "Parameter Learning"):
            if (Query == "none"):
                solver = pasta_solver.Pasta("tmpFile.lp","")
            else:
                solver = pasta_solver.Pasta("tmpFile.lp", Query)
            if request.form.get("Upper"):
                Upper = True
            else:
                Upper=False

            with Capturing() as answer:
                solver.parameter_learning(Upper)

            return render_template("sitoHTML.html",CodeOut = answer)

        #####################################################################
        else:
            return "SOMETHING WENT WRONG: ERROR CODE(1)"

    return "SOMETHING WENT WRONG: ERROR CODE(2)"