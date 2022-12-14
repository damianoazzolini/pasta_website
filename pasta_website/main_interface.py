from flask import render_template, request, flash, Blueprint
import sys

from pasta_website.__init__ import *
from pasta_website.db import get_db
from io import StringIO
#sys.path.append("venv/lib/python3.8/site-packages/pasta_website/pasta/pasta")              #used when creating the build for a virtualenv
sys.path.insert(0,"/mnt/c/Users/admin/Desktop/progettino/pasta_website/pasta/pasta")        #if you run it with Apache2 (MUST CHANGE TO YOUR ACTUAL PATH)         
#sys.path.append("pasta/pasta")                                                             #if you run it with flask wsgi server        
import pasta_solver

bp = Blueprint('main_interface', __name__, url_prefix='/')

class arguments: #for approximate inference
    rejection : bool
    mh : bool
    gibbs : bool
    block : int

@bp.route("/", methods=["POST","GET"]) 
def sitoHTML():

    if request.method == "GET":             #### GET call
        return render_template("sitoHTML.html")

    elif request.method == "POST":          #### POST call
        old_stdout = sys.stdout             #redirect stdout
        sys.stdout = mystdout = StringIO()

        db = get_db()
        answer =""
        ProgramCode = str(request.form["inputPr"])      #1 textbox
        Query = str(request.form["inputQ"])             #2 textbox
        Evidence = str(request.form["inputEv"])         #3 textbox
        RadioButton1 = str(request.form["options"])     #one of 5 radio button
        Inconsistent = bool(request.form.get("inconsistent"))
        Normalize = bool(request.form.get("normalize"))
        Upper = bool(request.form.get("Upper"))

        RadioButton2 = "none"
        nSamples = 0
        Blocks = 0
        if (not RadioButton1):
            flash("SELECT ONE OPTIONS!")    #porbably not needed - handled by HTML page
        if (not Query and RadioButton1!="Parameter Learning"):
            flash("QUERY MUST BE FILLED")

        with open('tmpFile.lp', 'w') as f:
            f.write(ProgramCode)
        
        try:
            #####################################################################
            #                           EXACT INFERENCE                         #
            #####################################################################
            if (RadioButton1 == "Exact Inference"):
                if (not Evidence):
                    solver = pasta_solver.Pasta("", Query)
                else:
                    solver = pasta_solver.Pasta("", Query, Evidence)
                
                solver.stop_if_inconsistent = Inconsistent
                solver.normalize_prob = Normalize
                lp, up = solver.inference(ProgramCode)      
                answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                        "\n" + "Upper probability for the query " +  Query + ": " + str(up))

            #####################################################################
            #                        APPROXIMATE INFERENCE                      #
            #####################################################################
            elif (RadioButton1 == "Approximate Inference"):
                args = arguments
                nSamples = int(request.form["nSamples"])

                if (not Evidence):
                    Evidence = ""
                    args.rejection  = False
                    args.mh         = False
                    args.gibbs      = False
                    args.block      = 0
                else:
                    RadioButton2 = str(request.form["AI_options"])
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

                solver = pasta_solver.Pasta("", Query, Evidence, False, False, nSamples)
                solver.stop_if_inconsistent = Inconsistent
                solver.normalize_prob = Normalize
                lp, up = solver.approximate_solve(args, ProgramCode)
                answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                        "\n" + "Upper probability for the query " +  Query + ": " + str(up))
                
            #####################################################################
            #                           MAP INFERENCE                           #
            #####################################################################
            elif (RadioButton1 == "Map Inference"):
                solver = pasta_solver.Pasta("", Query)    
                solver.stop_if_inconsistent = Inconsistent
                solver.normalize_prob = Normalize
                
                if Upper:
                    solver.consider_lower_prob = False
                """
                if (Upper and not (Normalize or Inconsistent)) and Solver:
                    max_p, atoms_list = solver.upper_mpe_inference(ProgramCode)
                else: 
                    max_p, atoms_list = solver.map_inference(ProgramCode)
                """
                max_p, atoms_list = solver.map_inference(ProgramCode)
                map_op = len(atoms_list) > 0 and len(atoms_list[0]) == len(solver.interface.prob_facts_dict)
                map_or_mpe = "MPE" if map_op else "MAP"
                answer = f"{map_or_mpe}: {max_p}\n{map_or_mpe} states: {len(atoms_list)}" + "\n"
                for i, el in enumerate(atoms_list):
                    answer += (f"State {i}: {el}") + "\n"

            #####################################################################
            #                               ABDUCTION                           #
            #####################################################################
            elif (RadioButton1 == "Abduction"):
                
                solver = pasta_solver.Pasta("", Query)
                solver.stop_if_inconsistent = Inconsistent
                solver.normalize_prob = Normalize
                    
                lp, up, abd_explanations = solver.abduction(ProgramCode)
                abd_exp_no_dup = pasta_solver.Pasta.remove_dominated_explanations(abd_explanations)
                
                if len(abd_exp_no_dup) > 0 and up != 0:
                    if Upper:
                        answer= f"Upper probability for the query: {up}"
                    else:
                        answer = ("Lower probability for the query " + Query + ": " + str(lp) + 
                            "\n" + "Upper probability for the query " +  Query + ": " + str(up))
                n_exp = sum(1 for ex in abd_exp_no_dup if len(ex) > 0)
                answer += "\n" + f"Abductive explanations: {n_exp}"

            #####################################################################
            #                         PARAMETER LEARNING                        #
            #####################################################################
            elif (RadioButton1 == "Parameter Learning"):

                #if (Query == "none"):
                #    solver = pasta_solver.Pasta("", "")
                #else:
                #    solver = pasta_solver.Pasta("", Query)
                #
                #if Upper:
                #    solver.consider_lower_prob = False
                #
                #solver.stop_if_inconsistent = Inconsistent
                #solver.normalize_prob = Normalize
                #solver.parameter_learning(ProgramCode)

                #------------------------------------
                if (Query == "none"):
                    solver = pasta_solver.Pasta("tmpFile.lp", "")
                else:
                    solver = pasta_solver.Pasta("tmpFile.lp", Query)

                if Upper:
                    solver.consider_lower_prob = False

                solver.stop_if_inconsistent = Inconsistent
                solver.normalize_prob = Normalize
                solver.parameter_learning()
                #------------------------------------

                answer = mystdout.getvalue()
            #####################################################################
            else:
                raise Exception("OPTION 1 ERROR (CASE)")
            errore = "ALL OK"

        except Exception as error:  #catch standard exceptions
            flash("OPS! SOMETHING WENT WRONG")
            errore = "EXCEPTION ERROR: " + str(error.args)
            answer += errore
        except:                     #catch other exceptions
            errore = "UNUSUAL ERROR: " + str(sys.exc_info()) + "\ncheck that inputs are correct"
            answer += errore
        
        finally:
            sys.stdout = old_stdout
            if (RadioButton1 == "Parameter Learning"): #warnings are already on 'answer' for PL
                warnings_stdout = ""
            else:
                warnings_stdout = mystdout.getvalue()
                #remove colors of stdout
                warnings_stdout = warnings_stdout.replace('\033[91m','')
                warnings_stdout = warnings_stdout.replace('\033[93m','')
                warnings_stdout = warnings_stdout.replace('\033[0m','')
            
            if (warnings_stdout != ""): #if there are warnings split them away from the answer
                warnings_stdout = "\n\n######################################\n\n" + warnings_stdout
            
            try:
                db.execute(
                    "INSERT INTO Request (program    , query, evidence, option_1         , option_2    , nSamples     , blocks     , upper     , errors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (ProgramCode, Query, Evidence, str(RadioButton1), RadioButton2, str(nSamples), str(Blocks), str(Upper), errore)
                )
                db.commit()
            except:
                print("\nERRORE DATABASE !!!")

        return render_template("sitoHTML.html",CodeOut = answer + warnings_stdout) 