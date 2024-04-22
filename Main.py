import mysql.connector
from tkinter import *
import sys,os
from picamera2 import Picamera2
import face_recognition
from face_recognition_identify import show_camera
from face_recognition_validifier import validify
from registerbio import register
import time
from datetime import datetime
from generer_lonning import get_html_template,generate
from tkinter import messagebox



mydatabase=mysql.connector.connect(host='host',port='port',user='user',passwd='password',db='database',charset='utf8',use_unicode=True)
def progressBar(count_value, total, suffix=''):
        bar_length = 100
        filled_up_length = int(round(bar_length * count_value / float(total)))
        percentage = round(100.0 * count_value / float(total), 1)
        bar = '=' * filled_up_length + '-' * (bar_length - filled_up_length)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percentage, '%', suffix))
        sys.stdout.flush()

#ROOF

#level 4 upper
def facerec_def_bruke1():
    def logout(ID):
        lbl_out=Label(facelogout_window,text='Vennligst vent')
        lbl_out.grid(row=1,column=1,padx=20,pady=20,sticky=S)
        
        identificator_cursor=mydatabase.cursor()
        identificator_query=("""SELECT RegID from Statusen
                                     WHERE AnsattID=%s""")
        identificator_data=ID
        identificator_cursor.execute(identificator_query%identificator_data)
        RegID=identificator_cursor.fetchone()
        RegID=RegID[0]
        identificator_cursor.close()

        temp_cursor=mydatabase.cursor()
        temp_query=("select Starttid from Arbeidsregistrering Where RegID=%s")
        temp_data=RegID
        temp_cursor.execute(temp_query%temp_data)
        sttid=temp_cursor.fetchone()
        temp_cursor.close()
        
        

        print (temp_data)
        slutttid=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        input_cursor=mydatabase.cursor()
        inputquery=("""
                    UPDATE Arbeidsregistrering 
                    SET Slutttid=%s,
                    Antalltimer=ROUND(TIMESTAMPDIFF(MINUTE, %s, %s) / 60.0, 1)
                    WHERE RegID=%s;
                    """ )
        inputdata=(slutttid,sttid[0],slutttid,temp_data)
        input_cursor.execute(inputquery,inputdata)
        input_cursor.close()

        log_cursor=mydatabase.cursor()
        query=("""UPDATE Statusen 
                    SET Statusen=%s,
                     RegID=NULL
                    WHERE AnsattID=%s""")
        data=("Jobber ikke",ID)
        log_cursor.execute(query,data)
        mydatabase.commit()
        log_cursor.close()
        facelogout_window.destroy()

        

    print ("Jeg jobber atm")
    facelogout_window=Toplevel()
    facelogout_window.title('Facerecognition logg ut')
    btn_facerec=Button(facelogout_window,width=50, height=20,bg='#fff7e6',text='Logg ut',command=lambda : logout(id))
    btn_facerec.grid(row=0,column=0,sticky=W)


def facerec_def_bruke2():
    def login(ID):
        log_cursor=mydatabase.cursor()
        lbl_in=Label(facelogin_window,text='Vennligst vent')
        lbl_in.grid(row=1,column=1,padx=20,pady=20,sticky=S)
        

        
        
        timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        temp_cursor=mydatabase.cursor()
        temp_cursor.execute("SELECT MAX(RegID) from Arbeidsregistrering")
        resultat=temp_cursor.fetchone()
        temp_cursor.close()
        RegID=resultat[0]
        print (RegID)
        RegID=int(RegID)+1
        RegID=str(RegID)

        dato=time.strftime('%Y-%m-%d')
        log_cursor2=mydatabase.cursor()
        query1=("""INSERT INTO Arbeidsregistrering (AnsattID,RegID,Dato,Starttid)
               values (%s,%s,%s,%s)""")
        data1=(ID,RegID,dato,timestamp)

        log_cursor2.execute(query1,data1)
        log_cursor2.close()
        query=("""UPDATE Statusen 
                    SET Statusen=%s,
                    RegID=%s
                    WHERE AnsattID=%s""")
        data=("Jobber",RegID,ID)
        log_cursor.execute(query,data)
        mydatabase.commit()
        facelogin_window.destroy()
        log_cursor.close()




    
    print ("jeg jobber ikke atm")
    facelogin_window=Toplevel()
    facelogin_window.title('Facerecognition logg inn')
    btn_facerec=Button(facelogin_window,width=50, height=20,bg='#fff7e6',text='Logg inn',command=lambda :login(id))
    btn_facerec.grid(row=0,column=0,sticky=W)

#level 4 Lower

#Level 3 Upper

def facerec_def_registrere():

    facereg_window=Toplevel()
    facereg_window.title('Facerecognition registrer')

    def reg(id_reg):
        
        
        confirm_cursor=mydatabase.cursor()
        query=(""" select Fornavn from Ansatt
                    where AnsattID=%s""")
        data=id_reg
        confirm_cursor.execute(query%data)
        test=confirm_cursor.fetchone()
        confirm_cursor.close()
        if test:
            register(id_reg,picam2)
            facereg_window1=Toplevel()
            facereg_window1.title('Facerecognition finish')
            messagebox.showinfo("Progress","Bildene blir na kvalitetsjekket")
            validify()
            
            facereg_window1.destroy()
            facereg_window.destroy()
            messagebox.showinfo("Popup", "Prosess utført og vellykket!")
            


        else:
            messagebox.showinfo("Popup", "Ansatt ikke funnet")
            facereg_window.destroy()

            







            

    aID=StringVar()
    ent_id=Entry(facereg_window, width = 20,textvariable=aID)
    ent_id.grid(row=0, column = 1, padx = 5, pady = 15,sticky=W)
    lbl_id = Label(facereg_window, text = 'Oppgi AnsattID' )
    lbl_id.grid(row = 0, column = 0, padx = 5, pady = 15,sticky=W)
    btn_submit=Button(facereg_window,bg='green',text='Submit',command=lambda : reg(aID.get()))
    btn_submit.grid(row=0,column=2,padx=5,pady=25,sticky=E)
    

def facerec_def_bruke():
    global id
    id=show_camera(known_faces,known_faces_folder,picam2)
    status_marker=mydatabase.cursor()
    query=('''SELECT Statusen FROM Statusen WHERE AnsattID=%s''')
    status_marker.execute(query%id)
    result_status=status_marker.fetchone()
    status_marker.close()
    if result_status[0]=="Jobber ikke":
        facerec_def_bruke2()
    elif result_status[0]=="Jobber":
        facerec_def_bruke1()
    else:
        messagebox.showerror("Error")
    



    return id




def oversikt_def_alle_ansatte():
    oversikt_ansatte_window=Toplevel()
    oversikt_ansatte_window.title('Oversikt alle ansatte')

    

    def find_ansatte():
        if ansattid.get()!='':
            
            ansettelsesdato.set("")
            fornavn.set("")
            etternavn.set("")
            telefonnummer.set("")
            stilling.set("")
            stillingstype.set("")
            find_cursor=mydatabase.cursor()
            query=('''select Ansatt.AnsattID,Ansettelsesdato,Fornavn,Etternavn,Telefon,Stilling,Stillingstype from Ansatt
            inner join Stilling on Stilling.AnsattID=Ansatt.AnsattID
            WHERE Ansatt.ansattID=%s''')
            data=(ansattid.get())
            find_cursor.execute(query%data)
            for row in find_cursor:
                ansattid.set(row[0])
                ansettelsesdato.set(row[1])
                fornavn.set(row[2])
                etternavn.set(row[3])
                telefonnummer.set(row[4])
                stilling.set(row[5])
                stillingstype.set(row[6])
            find_cursor.close()

        else:
            messagebox.showerror("Error", "Ingen ansatte med denne IDen")
    label_ansatt_id = Label(oversikt_ansatte_window, text="AnsattID")
    label_ansatt_id.grid(row=0, column=0, padx=10, pady=5, sticky=W)

    label_ansettelsesdato = Label(oversikt_ansatte_window, text="Ansettelsesdato")
    label_ansettelsesdato.grid(row=1, column=0, padx=10, pady=5, sticky=W)

    label_fornavn = Label(oversikt_ansatte_window, text="Fornavn")
    label_fornavn.grid(row=2, column=0, padx=10, pady=5, sticky=W)

    label_etternavn = Label(oversikt_ansatte_window, text="Etternavn")
    label_etternavn.grid(row=3, column=0, padx=10, pady=5, sticky=W)

    label_telefonnummer = Label(oversikt_ansatte_window, text="Telefonnummer")
    label_telefonnummer.grid(row=4, column=0, padx=10, pady=5, sticky=W)

    label_stilling = Label(oversikt_ansatte_window, text="Stilling")
    label_stilling.grid(row=5, column=0, padx=10, pady=5, sticky=W)

    label_stillingstype = Label(oversikt_ansatte_window, text="Stillingstype")
    label_stillingstype.grid(row=6, column=0, padx=10, pady=5, sticky=W)
    
    ansattid=StringVar()
    ansettelsesdato=StringVar()
    fornavn=StringVar()
    etternavn=StringVar()
    telefonnummer=StringVar()
    stilling=StringVar()
    stillingstype=StringVar()
    # Entry widgets
    entry_ansatt_id = Entry(oversikt_ansatte_window,textvariable=ansattid)
    entry_ansatt_id.grid(row=0, column=1, padx=10, pady=5)

    entry_ansettelsesdato = Entry(oversikt_ansatte_window,textvariable=ansettelsesdato,state='readonly')
    entry_ansettelsesdato.grid(row=1, column=1, padx=10, pady=5)

    entry_fornavn = Entry(oversikt_ansatte_window,textvariable=fornavn,state='readonly')
    entry_fornavn.grid(row=2, column=1, padx=10, pady=5)

    entry_etternavn = Entry(oversikt_ansatte_window,textvariable=etternavn,state='readonly')
    entry_etternavn.grid(row=3, column=1, padx=10, pady=5)

    entry_telefonnummer = Entry(oversikt_ansatte_window,textvariable=telefonnummer,state='readonly')
    entry_telefonnummer.grid(row=4, column=1, padx=10, pady=5)

    entry_stilling = Entry(oversikt_ansatte_window,textvariable=stilling,state='readonly')
    entry_stilling.grid(row=5, column=1, padx=10, pady=5)

    entry_stillingstype = Entry(oversikt_ansatte_window,textvariable=stillingstype,state='readonly')
    entry_stillingstype.grid(row=6, column=1, padx=10, pady=5)

    # Search button
    search_button = Button(oversikt_ansatte_window, text="Søk", command=find_ansatte)
    search_button.grid(row=7, column=0, columnspan=2, pady=10)

def regansatt():
    regansatt_window=Toplevel()
    regansatt_window.title("Registrer ansatt")
    def reg():
        check_cursor=mydatabase.cursor()
        check_cursor.execute('''select max(AnsattID) from Ansatt ''')
        tempid=check_cursor.fetchone()
        tempid=tempid[0]
        ansattid=int(tempid)+1
        dato=time.strftime('%Y-%m-%d')
        check_cursor.close()




        reg_ansatt_cursor=mydatabase.cursor()
        reg_query=('''INSERT INTO Ansatt VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''')
        reg_data=(ansattid,dato,fornavn.get(),etternavn.get(),fodselsnummer.get(),adresse.get(),telefon.get(),epost.get())
        reg_ansatt_cursor.execute(reg_query,reg_data)
        reg_ansatt_cursor.close()
        time.sleep(2)
        reg_stilling_cursor=mydatabase.cursor()
        reg_stilling_query=('''INSERT INTO Stilling values (%s,%s,%s,%s)''')
        reg_stilling_data=(ansattid,stilling.get(),timelonn.get(),stillingstype.get())
        reg_stilling_cursor.execute(reg_stilling_query,reg_stilling_data)
        reg_stilling_cursor.close()
        reg_status_cursor=mydatabase.cursor()
        reg_status_query=('''INSERT INTO Statusen VALUES (%s,%s,%s) ''')
        reg_status_data=(ansattid,"Jobber ikke","NULL")
        reg_status_cursor.execute(reg_status_query,reg_status_data)
        reg_status_cursor.close()

        mydatabase.commit()
        messagebox.showinfo("Suksess", f"Ansatt {fornavn.get()} {etternavn.get()} er registrert med ansattID {ansattid}")

        





        
    fornavn=StringVar()
    etternavn=StringVar()
    fodselsnummer=StringVar()
    adresse=StringVar()
    telefon=StringVar()
    epost=StringVar()
    stilling=StringVar()
    timelonn=StringVar()
    stillingstype=StringVar()
    fornavn_label = Label(regansatt_window, text="Fornavn:")
    fornavn_label.grid(row=0, column=0, padx=5, pady=5)

    fornavn_entry = Entry(regansatt_window,textvariable=fornavn)
    fornavn_entry.grid(row=0, column=1, padx=5, pady=5)

    etternavn_label = Label(regansatt_window, text="Etternavn:")
    etternavn_label.grid(row=1, column=0, padx=5, pady=5)

    etternavn_entry = Entry(regansatt_window,textvariable=etternavn)
    etternavn_entry.grid(row=1, column=1, padx=5, pady=5)

    fodselsnummer_label = Label(regansatt_window, text="Fødselsnummer:")
    fodselsnummer_label.grid(row=2, column=0, padx=5, pady=5)

    fodselsnummer_entry = Entry(regansatt_window,textvariable=fodselsnummer)
    fodselsnummer_entry.grid(row=2, column=1, padx=5, pady=5)

    adresse_label = Label(regansatt_window, text="Adresse:")
    adresse_label.grid(row=3, column=0, padx=5, pady=5)

    adresse_entry = Entry(regansatt_window,textvariable=adresse)
    adresse_entry.grid(row=3, column=1, padx=5, pady=5)

    telefon_label = Label(regansatt_window, text="Telefon:")
    telefon_label.grid(row=4, column=0, padx=5, pady=5)

    telefon_entry = Entry(regansatt_window,textvariable=telefon)
    telefon_entry.grid(row=4, column=1, padx=5, pady=5)

    epost_label = Label(regansatt_window, text="Epost:")
    epost_label.grid(row=5, column=0, padx=5, pady=5)

    epost_entry = Entry(regansatt_window,textvariable=epost)
    epost_entry.grid(row=5, column=1, padx=5, pady=5)

    stilling_label = Label(regansatt_window, text="Stilling:")
    stilling_label.grid(row=6, column=0, padx=5, pady=5)

    stilling_entry = Entry(regansatt_window,textvariable=stilling)
    stilling_entry.grid(row=6, column=1, padx=5, pady=5)

    timelonn_label = Label(regansatt_window, text="Timelønn:")
    timelonn_label.grid(row=7, column=0, padx=5, pady=5)

    timelonn_entry = Entry(regansatt_window,textvariable=timelonn)
    timelonn_entry.grid(row=7, column=1, padx=5, pady=5)

    stillingstype_label = Label(regansatt_window, text="Stillingstype:")
    stillingstype_label.grid(row=8, column=0, padx=5, pady=5)

    stillingstype_entry = Entry(regansatt_window,textvariable=stillingstype)
    stillingstype_entry.grid(row=8, column=1, padx=5, pady=5)

    # Create a button to register the user
    register_button = Button(regansatt_window, text="Registrer", command=reg)
    register_button.grid(row=9, column=0, columnspan=2, pady=10)

def oversikt_def_arbeider_na():
    oversikt_arbeider_window=Toplevel()
    oversikt_arbeider_window.title('Oversikt alle ansatte som jobber nå')
    def eventdef(event):
        chosen=employees_listbox.get(employees_listbox.curselection())
        event_cursor=mydatabase.cursor()
        
        query1=('''SELECT AnsattID,Fornavn,Etternavn FROM Ansatt
                ''')
        
        event_cursor.execute(query1)
        for rows in event_cursor:


            if chosen[0]==rows[0]:
                ansattid.set(rows[0])
                fornavn.set(rows[1])
                etternavn.set(rows[2])
                status.set('Jobber')
        event_cursor.close()
                
    
    fornavn=StringVar()
    etternavn=StringVar()
    ansattid=StringVar()
    status=StringVar()
    aktiveansatte=[]
    
    set_cursor=mydatabase.cursor()
    query=('''SELECT Ansatt.AnsattID
                             from Ansatt 
                             inner join Statusen on Ansatt.AnsattID=Statusen.AnsattID
                             WHERE Statusen.Statusen=%s''')
    data=("Jobber",)
    set_cursor.execute(query,data)
    for row in set_cursor:
        aktiveansatte+=row[0]
    set_cursor.close()

            
    title_label = Label(oversikt_arbeider_window, text="Jobber nå", font=("Helvetica", 16))
    title_label.grid(row=0,column=1,pady=10,padx=10)
    label_ansattid = Label(oversikt_arbeider_window, text="Ansatt ID")
    label_ansattid.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    entry_ansattid = Entry(oversikt_arbeider_window,textvariable=ansattid,state='readonly')
    entry_ansattid.grid(row=0, column=1, padx=10, pady=5)

    # Labels and Entry widgets for Fornavn
    label_fornavn = Label(oversikt_arbeider_window, text="Fornavn")
    label_fornavn.grid(row=1, column=0, padx=10, pady=5, sticky=W)
    entry_fornavn = Entry(oversikt_arbeider_window,textvariable=fornavn,state='readonly')
    entry_fornavn.grid(row=1, column=1, padx=10, pady=5)

    # Labels and Entry widgets for Etternavn
    label_etternavn = Label(oversikt_arbeider_window, text="Etternavn")
    label_etternavn.grid(row=2, column=0, padx=10, pady=5, sticky=W)
    entry_etternavn = Entry(oversikt_arbeider_window,textvariable=etternavn,state='readonly')
    entry_etternavn.grid(row=2, column=1, padx=10, pady=5)

    # Labels and Entry widgets for Status
    label_status = Label(oversikt_arbeider_window, text="Status")
    label_status.grid(row=3, column=0, padx=10, pady=5, sticky=W)
    entry_status = Entry(oversikt_arbeider_window,textvariable=status,state='readonly')
    entry_status.grid(row=3, column=1, padx=10, pady=5)


    # Listbox to display employee information
    
    
    list_employees=StringVar()
    employees_listbox = Listbox(oversikt_arbeider_window, width=40, height=10,listvariable=list_employees)
    employees_listbox.grid(row=0, column=2, rowspan=5, padx=10, pady=5)
    list_employees.set(tuple(aktiveansatte))

    employees_listbox.bind('<<ListboxSelect>>',eventdef)



def lonning_def_se():
    se_lonning_window=Toplevel()
    se_lonning_window.title('Se lønninger')

    def windowevent(event):
        chosen=lst_lonninger.get(lst_lonninger.curselection())
        event_cursor=mydatabase.cursor()
        event_cursor.execute('''SELECT DokumentID,Opprettelsesdato,Utbetalingsstatus,Dokument_Navn,Dokument_Sti,Beløp from Lønnsdokument''')
        for row in event_cursor:
            if (chosen[0])==(row[3]):
                dokument_id.set(row[0])
                opprettelsesdato.set(row[1])
                utbetalingsstatus.set(row[2])
                dokument_navn.set(row[3])
                dokument_sti.set(row[4])
                belop.set(row[5])
        event_cursor.close()


    def find():
        temp_var1=fra_dato.get()
        temp_var2=til_dato.get()
        temp_var3=ansattid.get()
        if (temp_var1=="") or (temp_var2=="") or (temp_var3==""):
            messagebox.showerror("Error", "Fyll alle felt!")
        else:
            
            find_cursor=mydatabase.cursor()
            query=('''SELECT Dokument_Navn  FROM Lønnsdokument WHERE Opprettelsesdato>%s and Opprettelsesdato<%s and AnsattID=%s''')
            data=(fra_dato.get(),til_dato.get(),ansattid.get())
            find_cursor.execute(query,data)
            lonninger=[]
            for rows in find_cursor:
                lonninger+=[rows]
                print (rows)
            find_cursor.close()

            list_lonning.set(tuple(lonninger))

    def reset():
        lonninger=[]
        list_lonning.set(tuple(lonninger))
        dokument_id.set('')
        opprettelsesdato.set('')
        utbetalingsstatus.set('')
        dokument_navn.set('')
        dokument_sti.set('')
        belop.set('')
        ansattid.set('')


            
                

                
    y_scroll=Scrollbar(se_lonning_window,orient=VERTICAL)
    y_scroll.grid(row=3,column=3,rowspan=2,padx=(0,200),pady=5,sticky=NS)
    #stringvars
    ansattid=StringVar()
    fra_dato=StringVar()
    til_dato=StringVar()
    opprettelsesdato=StringVar()
    utbetalingsstatus=StringVar()
    dokument_navn=StringVar()
    dokument_sti=StringVar()
    belop=StringVar()
    dokument_id=StringVar()
    list_lonning=StringVar()
    lonninger=[]
    

    #entries
    entry_ansattid = Entry(se_lonning_window,textvariable=ansattid)
    entry_fra_dato = Entry(se_lonning_window,textvariable=fra_dato)
    entry_til_dato = Entry(se_lonning_window,textvariable=til_dato)
    entry_opprettelsesdato = Entry(se_lonning_window,state='readonly',textvariable=opprettelsesdato)
    entry_utbetalingsstatus = Entry(se_lonning_window,state='readonly',textvariable=utbetalingsstatus)
    entry_dokument_navn = Entry(se_lonning_window,state='readonly',textvariable=dokument_navn)
    entry_dokument_sti = Entry(se_lonning_window,state='readonly',textvariable=dokument_sti)
    entry_belop = Entry(se_lonning_window,state='readonly',textvariable=belop)
    entry_dokument_id = Entry(se_lonning_window,state='readonly',textvariable=dokument_id)
    lst_lonninger=Listbox(se_lonning_window,width=20,height=15,listvariable=list_lonning,yscrollcommand=y_scroll.set)
    y_scroll["command"]=lst_lonninger.yview
    

    # Labels
    Label(se_lonning_window, text='Fra dato (yyyy-mm-dd):').grid(row=0, column=2, pady=5,sticky=W)
    Label(se_lonning_window, text='Til dato (yyyy-mm-dd):').grid(row=1, column=2,sticky=W)
    Label(se_lonning_window, text='AnsattID').grid(row=0, column=0, padx=5, pady=5,sticky=W)
    Label(se_lonning_window, text='Opprettelsesdato:').grid(row=1, column=0, padx=5, pady=5,sticky=W)
    Label(se_lonning_window, text='Utbetalingsstatus:').grid(row=2, column=0, padx=5, pady=5,sticky=W)
    Label(se_lonning_window, text='Dokument_Navn:').grid(row=3, column=0, padx=5, pady=5,sticky=W)
    Label(se_lonning_window, text='Dokument_Sti:').grid(row=4, column=0, padx=5, pady=5,sticky=W)
    Label(se_lonning_window, text='Belop:').grid(row=5, column=0, padx=5, pady=5,sticky=W)
    Label(se_lonning_window, text='DokumentID:').grid(row=6, column=0, padx=5, pady=5,sticky=W)

    # Entry field placements
    entry_ansattid.grid(row=0, column=1, padx=5, pady=5,sticky=W)
    entry_fra_dato.grid(row=0, column=3,sticky=W)
    entry_til_dato.grid(row=1, column=3,sticky=W)
    entry_opprettelsesdato.grid(row=1, column=1, padx=5, pady=5)
    entry_utbetalingsstatus.grid(row=2, column=1, padx=5, pady=5)
    entry_dokument_navn.grid(row=3, column=1, padx=5, pady=5)
    entry_dokument_sti.grid(row=4, column=1, padx=5, pady=5)
    entry_belop.grid(row=5, column=1, padx=5, pady=5)
    entry_dokument_id.grid(row=6, column=1, padx=5, pady=5)
    lst_lonninger.grid(row=3,column=2,rowspan=2,pady=5,padx=6)
    lst_lonninger.bind('<<ListboxSelect>>',windowevent)

    # Submit button
    submit_button = Button(se_lonning_window, text="Finn", command=find,bg='green')
    reset_button = Button(se_lonning_window, text="Reset", command=reset,bg='yellow')
    submit_button.grid(row=7, column=4, columnspan=1,padx=5)
    reset_button.grid(row=7, column=3, columnspan=1, pady=5,sticky=E)
def lonning_def_generer():
    generer_lonning_window=Toplevel()
    generer_lonning_window.title('Generer lønning')
    def submit():
        ansattid = entry_employee_id.get()
        info_cursor=mydatabase.cursor()
        query=('''SELECT Fornavn,Etternavn,Stilling.Stilling,Timelonn
                from Ansatt inner join Stilling on Ansatt.Ansattid=Stilling.Ansattid
                where Ansatt.Ansattid=%s''')
        data=ansattid
        info_cursor.execute(query%data)
        for index in info_cursor:
            fornavn=index[0]
            etternavn=index[1]
            stilling=index[2]
            timelonn=index[3]
        info_cursor.close()
        
        try:

            datostart = entry_date_start.get()
            datoslutt = entry_date_end.get()
            skatteprosent = entry_skatteprosent.get()
            timer_cursor=mydatabase.cursor()
            query_timer=('''SELECT SUM(AntallTimer) as AntallTimer
                        from Arbeidsregistrering
                        where Ansattid=%s and Dato>%s and Dato<%s
    ''')
            data_timer=(ansattid,datostart,datoslutt)
            timer_cursor.execute(query_timer,data_timer)
            antall_timer=timer_cursor.fetchone()
            timer_cursor.close()
            antall_timer=antall_timer[0]
            timelonn, skatteprosent = map(float, [timelonn, skatteprosent])
            brutto_lonn=antall_timer*timelonn
            

            skatteprosent=skatteprosent/100
            trekk=1-skatteprosent
            netto_lonn=brutto_lonn*trekk
            netto_lonn=f"{netto_lonn:.2f}"
            brutto_lonn=f"{brutto_lonn:.2f}"
            timelonn=f"{timelonn:.2f}"
            today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            docid_cursor=mydatabase.cursor()
            docid_cursor.execute("""select max(DokumentID) from Lønnsdokument""")
            maxdocid=docid_cursor.fetchone()
            maxdocid=maxdocid[0]
            finaldocid=int(maxdocid)+1
            docid_cursor.close()


            
            fullname=f"{fornavn} {etternavn}"
            html_template=get_html_template()
            sti,filnavn=generate (html_template,datostart,datoslutt,ansattid,fullname,stilling,\
                          timelonn,antall_timer,brutto_lonn,skatteprosent,\
                          netto_lonn)
            
            insert_cursor=mydatabase.cursor()
            insert_query=('''INSERT INTO Lønnsdokument values 
                            (%s,%s,%s,%s,%s,%s,%s)''')
            data=(finaldocid,today,"Fullført",ansattid,filnavn,sti,netto_lonn)
            insert_cursor.execute(insert_query,data)
            mydatabase.commit()
            insert_cursor.close()
            messagebox.showinfo("Popup", f"Filen er opprettet hos {sti}")
            

            generer_lonning_window.destroy()

        except TypeError:
            print ('Ingen timer jobbet i denne perioden')
            messagebox.showerror("Error", "Ingen timer jobbet i denne perioden")
        except UnboundLocalError:
            print ('Ingen ansatte med den IDen')
            messagebox.showerror("Error", "Ingen ansatte med denne IDen")





    ansattid=StringVar()
    employee_id_label = Label(generer_lonning_window, text="AnsattID:")
    employee_id_label.grid(row=0, column=0, padx=5, pady=5)
    
    entry_employee_id = Entry(generer_lonning_window,textvariable=ansattid)
    entry_employee_id.grid(row=0, column=1, padx=5, pady=5)
    datostart=StringVar()
    date_start_label = Label(generer_lonning_window, text="Start Dato (yyyy-mm-dd):")
    date_start_label.grid(row=1, column=0, padx=5, pady=5)
    entry_date_start = Entry(generer_lonning_window,textvariable=datostart)
    entry_date_start.grid(row=1, column=1, padx=5, pady=5)
    datoslutt=StringVar() 
    date_end_label = Label(generer_lonning_window, text="Slutt Dato (yyyy-mm-dd):")
    date_end_label.grid(row=2, column=0, padx=5, pady=5)
    entry_date_end = Entry(generer_lonning_window,textvariable=datoslutt)
    entry_date_end.grid(row=2, column=1, padx=5, pady=5)
    skatteprosent=StringVar()
    skatteprosent_label = Label(generer_lonning_window, text="Skatteprosent:")
    skatteprosent_label.grid(row=3, column=0, padx=5, pady=5)
    entry_skatteprosent = Entry(generer_lonning_window,textvariable=skatteprosent)
    entry_skatteprosent.grid(row=3, column=1, padx=5, pady=5)

    
    submit_button=Button(generer_lonning_window, text="Generer", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=5)

    


#Level 3 Lower


#Level 2 upper
def facerec_def():
    facerec_window=Toplevel()
    facerec_window.title('Facerecognition meny')


    btn_facerec=Button(facerec_window,width=50, height=20,bg='#fff7e6',text='Registrer biometri',command=facerec_def_registrere)
    btn_facerec.grid(row=0,column=0,sticky=W)

    btn_oversikt=Button(facerec_window,width=50, height=20,bg='#fff7e6',text='Logg inn/Logg ut',command=facerec_def_bruke)
    btn_oversikt.grid(row=0,column=1,sticky=W)



def oversikt_def():
    oversikt_window=Toplevel()
    oversikt_window.title('Admin meny')

    btn_oversikt=Button(oversikt_window,width=50, height=20,bg='#fff7e6',text='Vis alle ansatte',command=oversikt_def_alle_ansatte)
    btn_oversikt.grid(row=0,column=0,sticky=W)

    btn_oversikt1=Button(oversikt_window,width=50, height=20,bg='#fff7e6',text='Vis alle som jobber nå',command=oversikt_def_arbeider_na)
    btn_oversikt1.grid(row=0,column=1,sticky=W)

    btn_reg=Button(oversikt_window,width=50, height=20,bg='#fff7e6',text='Registrer ny ansatt',command=regansatt)
    btn_reg.grid(row=0,column=2,sticky=W)


def lonning_def():

    facelogout_window=Toplevel()
    facelogout_window.title('Facerecognition meny')

    btn_vis=Button(facelogout_window,width=50, height=20,bg='#fff7e6',text='Vis lønninger',command=lonning_def_se)
    btn_vis.grid(row=0,column=0,sticky=W)

    btn_generer=Button(facelogout_window,width=50, height=20,bg='#fff7e6',text='Generer lønning',command=lonning_def_generer)
    btn_generer.grid(row=0,column=1,sticky=W)



#LEVEL 2 LOWER

#LEVEL 1 UPPER
facereg_window=Tk()
facereg_window.title('meny')

btn_facerec=Button(facereg_window,width=50, height=20,bg='#fff7e6',text='Facerecognition',command=facerec_def)
btn_facerec.grid(row=0,column=0,sticky=W)

btn_oversikt=Button(facereg_window,width=50, height=20,bg='#fff7e6',text='Admin',command=oversikt_def)
btn_oversikt.grid(row=0,column=1,sticky=W)

btn_oversikt1=Button(facereg_window,width=50, height=20,bg='#fff7e6',text='Lønning',command=lonning_def)
btn_oversikt1.grid(row=0,column=2,sticky=W)
#LEVEL 1 LOWER


#GROUND LEVEL UPPER
known_faces_folder = "dataset"
known_faces = []

# Get the total number of files in the directory
total_files = len(os.listdir(known_faces_folder))

for count, file_name in enumerate(os.listdir(known_faces_folder), start=1):
    image_path = os.path.join(known_faces_folder, file_name)
    known_face_image = face_recognition.load_image_file(image_path)
    known_face_encoding = face_recognition.face_encodings(known_face_image)[0]
    known_faces.append(known_face_encoding)

        # Call the progressBar function to update the progress bar
    progressBar(count, total_files, suffix='Processing: {}'.format(file_name))

# Print a newline after the loop to move to the next line in the console
print("\nDone")
#gotten from https://www.geeksforgeeks.org/progress-bars-in-python/

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))




#GROUND LEVEL LOWER
facereg_window.mainloop()
mydatabase.close()
print ("Databasen er nå stengt")
