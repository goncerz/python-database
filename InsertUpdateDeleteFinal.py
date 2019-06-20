import tkinter
from tkinter import filedialog
import os
import datetime
import psycopg2


class App(tkinter.Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.create_widgets()
        
        
    def create_widgets(self):
        self.btnWidth = 30
        self.lblWidth = 120
        self.entWidth = 4
        self.padx = 10
        self.pady = self.padx
        
        self.rmin = 3 #minimal number of nonempty rows in selected .ods file (headers and at least 1 row)
        self.rmax = 100002 #maximal number of nonempty rows in selected file (with headers)
        #self.rlim = self.rmax #number of rows to get once
        self.rnum = 0 #number of nonempty rows in selected file (with headers)
        self.initDir = "~" #initial directory path"
        self.inputFile = ""
        self.scriptFile = ""
        self.logFile = ""
        self.c124 = "|"

        self.rbtnChoice = tkinter.StringVar()
        self.rbtnChoice.set(None)

        self.rbtnInsert = tkinter.Radiobutton(self)
        self.rbtnInsert["text"] = "INSERT"
        self.rbtnInsert["variable"] = self.rbtnChoice
        self.rbtnInsert["value"] = "insert"
        self.rbtnInsert["command"] = self.rbtn_change
        self.rbtnInsert.grid(row = 0, column = 0, padx = self.padx, pady = self.pady)

        self.rbtnUpdate = tkinter.Radiobutton(self)
        self.rbtnUpdate["text"] = "UPDATE"
        self.rbtnUpdate["variable"] = self.rbtnChoice
        self.rbtnUpdate["value"] = "update"
        self.rbtnUpdate["command"] = self.rbtn_change
        self.rbtnUpdate.grid(row = 0, column = 1, padx = self.padx, pady = self.pady)

        self.rbtnDelete = tkinter.Radiobutton(self)
        self.rbtnDelete["text"] = "DELETE"
        self.rbtnDelete["variable"] = self.rbtnChoice
        self.rbtnDelete["value"] = "delete"
        self.rbtnDelete["command"] = self.rbtn_change
        self.rbtnDelete.grid(row = 0, column = 2, padx = self.padx, pady = self.pady)

        self.lblpk = tkinter.Label(self)
        self.lblpk["text"] = "How many fields in primary key?"
        self.lblpk["width"] = self.btnWidth
        #row = 1, column = 1

        self.entpk = tkinter.Entry(self)
        self.entpk["text"] = ""
        self.entpk["width"] = self.entWidth
        self.entpk["background"] = "white"
        #row = 2, column = 1

        self.lbl = tkinter.Label(self)
        self.lbl["text"] = ""
        self.lbl["width"] = self.lblWidth
        self.lbl.grid(row = 3, column = 0, columnspan = 3, padx = self.padx, pady = self.pady)
        
        self.btnCheckFile = tkinter.Button(self)
        self.btnCheckFile["text"] = "Check file"
        self.btnCheckFile["command"] = self.check_file
        self.btnCheckFile["width"] = self.btnWidth
        self.btnCheckFile.grid(row = 4, column = 0, padx = self.padx, pady = self.pady)

        self.btnCreateScript = tkinter.Button(self)
        self.btnCreateScript["text"] = "Create script"
        self.btnCreateScript["command"] = self.create_script
        self.btnCreateScript["width"] = self.btnWidth
        self.btnCreateScript.grid(row = 4, column = 1, padx = self.padx, pady = self.pady)
        
        self.btnRunScript = tkinter.Button(self)
        self.btnRunScript["text"] = "Run script"
        self.btnRunScript["command"] = self.run_script
        self.btnRunScript["width"] = self.btnWidth
        self.btnRunScript.grid(row = 4, column = 2, padx = self.padx, pady = self.pady)

        self.lblpwd = tkinter.Label(self)
        self.lblpwd["text"] = "Database password:"
        self.lblpwd["width"] = self.btnWidth
        #row = 5, column = 2

        self.entpwd = tkinter.Entry(self)
        self.entpwd["text"] = ""
        self.entpwd["width"] = self.btnWidth
        self.entpwd["show"] = "*"
        self.entpwd["background"] = "white"
        #row = 6, column = 2

        self.disable_btnCreateScript()
        self.disable_btnRunScript()


    def enable_btnCheckFile(self):
        self.btnCheckFile["state"] = "normal"

    def disable_btnCheckFile(self):
        self.btnCheckFile["state"] = "disabled"


    def enable_btnCreateScript(self):
        if self.inputFile and self.rbtnChoice.get() != "None":
            self.btnCreateScript["state"] = "normal"

    def disable_btnCreateScript(self):
        self.btnCreateScript["state"] = "disabled"


    def enable_btnRunScript(self):
        if self.scriptFile:
            self.btnRunScript["state"] = "normal"
            self.show_pwd()

    def disable_btnRunScript(self):
        self.btnRunScript["state"] = "disabled"
        self.hide_pwd()
        

    def enable_rbtn(self):
        self.rbtnInsert["state"] = "normal"
        self.rbtnUpdate["state"] = "normal"
        self.rbtnDelete["state"] = "normal"

    def disable_rbtn(self):
        self.rbtnInsert["state"] = "disabled"
        self.rbtnUpdate["state"] = "disabled"
        self.rbtnDelete["state"] = "disabled"


    def show_pk(self):
        self.lblpk.grid(row = 1, column = 1, padx = self.padx, pady = self.pady)
        self.entpk.grid(row = 2, column = 1, padx = self.padx, pady = self.pady)

    def hide_pk(self):
        self.lblpk.grid_forget()
        self.entpk.grid_forget()


    def show_pwd(self):
        self.lblpwd.grid(row = 5, column = 2, padx = self.padx, pady = self.pady)
        self.entpwd.grid(row = 6, column = 2, padx = self.padx, pady = self.pady)

    def hide_pwd(self):
        self.lblpwd.grid_forget()
        self.entpwd.grid_forget()
        

    def rbtn_change(self):
        self.enable_btnCreateScript()
        if self.rbtnChoice.get() == "update":
            self.show_pk()
        else:
            self.hide_pk()

        
    def check_file(self):
        self.disable_btnRunScript()
        self.disable_btnCreateScript()
        self.disable_btnCheckFile()
        self.disable_rbtn()
        self.lbl["text"] = "Checking file .."
            
        self.inputFile = filedialog.askopenfilename(
            initialdir = self.initDir,
            title = "Select file",
            filetypes = (("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*"))
            )

        if self.inputFile:
            #chkstart = datetime.datetime.now()
            #print("Check file - start:", chkstart)
            
            try:
                with open(self.inputFile, "r") as f:

                    #1st line
                    lst1 = f.readline().strip().split(self.c124)
                    if not (lst1 and lst1[0]):
                        raise Exception("No table name in line 1")

                    tbl = lst1[0]
                    if not tbl[0].isalpha():
                        raise Exception("Incorrect table name in line 1 (" + tbl + ")")

                    self.rnum += 1

                    #2nd line
                    lst2 = f.readline().strip().split(self.c124)
                    if "" in lst2:
                        raise Exception("Incorrect structure of line 2 (field " + str(lst2.index("") + 1) + " empty)")

                    for field in lst2:
                        if not field[0].isalpha():
                            raise Exception("Incorrect field name (" + field + ") in line 2")

                    self.rnum += 1

                    #3rd and next lines
                    ln2 = len(lst2)

                    for line in f:
                        lst = line.strip().split(self.c124)
                        ln = len(lst)

                        if ln:
                            self.rnum += 1

                        if ln != ln2:
                            raise Exception("Incorrect length (" + str(ln) + ") of line " + str(self.rnum))
                      
                        if self.rnum > self.rmax:
                            raise Exception("Maximal number of lines (" + str(self.rmax) + ") exceeded")

                if self.rnum < self.rmin:
                    raise Exception("Incorrect number of lines (" + str(self.rnum) + ")")
                
                self.lbl["text"] = "File OK: " + self.inputFile
                self.enable_btnCreateScript()
                #chkstop = datetime.datetime.now()
                #print("Check file - stop:", chkstop)
                #print("Checking time:", chkstop - chkstart)
                
            except (IOError, Exception) as err:
                self.inputFile = ""
                self.scriptFile = ""
                self.rnum = 0
                self.lbl["text"] = err
            finally:
                self.enable_rbtn()
                self.enable_btnCheckFile()


    def create_script(self):
        cmd = self.rbtnChoice.get()
        initDir = os.path.dirname(self.inputFile)
        self.disable_btnRunScript()
        self.disable_btnCreateScript()
        self.disable_btnCheckFile()
        self.disable_rbtn()
        self.lbl["text"] = "Creating script .."
        
        try:
            if cmd != "insert" and cmd != "update" and cmd != "delete":
                raise Exception("Unknown command (" + cmd + ")")

            with open(self.inputFile, "r") as f:
                lst1 = f.readline().strip().split(self.c124)
                tbl = lst1[0]

                lst2 = f.readline().strip().split(self.c124)
                ln2 = len(lst2)

                if cmd == "update":
                    npk = self.entpk.get()
                    if not (npk.isdigit() and int(npk) and int(npk) < ln2):
                        raise Exception("Incorrect number of fields in primary key (" + npk + ")")

                self.scriptFile = initDir + "/" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + "_" + tbl + "_" + cmd + ".sql"
                
                with open(self.scriptFile, "w") as scr:
                    for line in f:
                        lst = line.replace("\n", "").split(self.c124)

                        if cmd == "insert":
                            stmt = "insert into " + tbl + "(" + ",".join(lst2) + ") values ('" + "','".join(lst) + "')"
                            stmt = stmt.replace("''", "null")

                        else:
                            sqllst = []

                            for i in range(0, ln2):
                                sqllst.append(lst2[i] + "='" + lst[i] + "'")

                            if cmd == "update":
                                npk = int(self.entpk.get())
                                stmt = "update " + tbl + " set " + ",".join(sqllst[npk:]).replace("''", "null")
                                stmt += " where " + " and ".join(sqllst[:npk]).replace("=''", " is null") 

                            else: #cmd == "delete"
                                stmt = "delete from " + tbl + " where " + " and ".join(sqllst).replace("=''", " is null")
                                
                        stmt += ";\n"
                        scr.write(stmt)

            self.enable_btnRunScript()
            self.lbl["text"] = "Done. Script file: " + self.scriptFile
                        
        except (IOError, Exception) as err:
            self.scriptFile = ""
            self.lbl["text"] = err
        finally:
            self.entpk.delete(0, tkinter.END)
            self.enable_rbtn()
            self.enable_btnCheckFile()
            self.enable_btnCreateScript()


    def run_script(self):
        db = "python"
        usr = "postgres"
        pwd = self.entpwd.get()
        hst = "127.0.0.1"
        prt = "5432"
        
        conn = ""

        self.disable_btnRunScript()
        self.disable_btnCreateScript()
        self.disable_btnCheckFile()
        self.disable_rbtn()
        self.lbl["text"] = "Running script .."
        
        try:
            conn = psycopg2.connect(
                dbname = db,
                user = usr,
                password = pwd,
                host = hst,
                port = prt
                )
            
            conn.set_session(autocommit = True)
            cur = conn.cursor()
            self.logFile = self.scriptFile + ".log"

            with open(self.scriptFile, "r") as scr:
                with open(self.logFile, "w") as lg:
                    for line in scr:
                        lg.write(line)

                        try:
                            cur.execute(line)
                            lg.write(cur.statusmessage + "\n")
                        except psycopg2.Error as e:
                            lg.write(str(e))
                        
            #conn.commit()
            cur.close()
            
            self.lbl["text"] = "Done. Log file: " + self.logFile
            self.inputFile = ""
            self.scriptFile = ""
            self.logFile = ""
            self.rbtnChoice.set(None)
            self.hide_pk()
            
        except (IOError, Exception, psycopg2.Error) as err:
            self.lbl["text"] = err
            self.enable_btnRunScript()
            self.enable_btnCreateScript()
            
        finally:
            if(conn):
                conn.close()

            self.entpwd.delete(0, tkinter.END)
            self.enable_rbtn()
            self.enable_btnCheckFile()


                
root = tkinter.Tk()
root.title("Insert / Update / Delete")
root.geometry("1000x500")
app = App(root)
root.mainloop()
