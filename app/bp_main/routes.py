from app import db
from flask_login import login_required
import pandas as pd
import sqlite3
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from app.bp_main.forms import UploadForm, TechnologyForm, ToolForm
from app.models import Tool, Technology, FCT

main = Blueprint('main', __name__, url_prefix='/main')


@main.before_request
@login_required
def login_required_for_all_request():
    pass


@main.route('/')
@main.route('/index', methods=["GET", "POST"])
def index():
    """
    1. Hompage für eingelogte User
    2. Dashboard und Datenbank-Ansicht
    3. Auswahl von Datenbank-Einträgen
    TODO Excel-Upload im Dashboard
    """
    show = True
    tools = Tool.query.order_by(Tool.id).limit(1).all()
    techs = Technology.query.order_by(Technology.created_on).limit(10).all()
    form = UploadForm()
    if request.method == "POST":
        print("I was here")
        processData(request)
    try:
        data, columns = readData()
    except:
        print(f"Noch kein Import vorhanden!")
        show = False
        data = None
        columns = None
    return render_template('main/dashboard.html', tools=tools, techs=techs, show=show, data=data, column_names=columns)


@main.route("/seed")
def seed():
    """
    Hilfsmethode um Datenbank zu füllen
    """
    try:
        Technology.seed(db.session)
        Tool.seed(db.session)
        return "Database seeded"
    except Exception as err:
        return str(err)

#
#  Business-Logic: Technologiekette modellieren
#


@main.route("/ft", methods=['GET', 'POST'])
def ft():

    technology = Technology.query.order_by(Technology.position).all()
    tool = Tool.query.first()
    if Tool.query.count() == 2:
        tool_roghness_old = Tool.query.get_or_404(2).roughness.replace(" µm", "").replace(",",".")
        tool_diameter_old = Tool.query.get_or_404(2).diameter.replace(" m", "").replace(",", ".")
        tool_width_old = Tool.query.get_or_404(2).width.replace(" m", "").replace(",", ".")
        tool_height_old = Tool.query.get_or_404(2).height.replace(" m", "").replace(",", ".")
        tool_length_old = Tool.query.get_or_404(2).length.replace(" m", "").replace(",", ".")
    else:
        tool_roghness_old = tool.roughness.replace(" µm", "").replace(",",".")
        tool_diameter_old = tool.diameter.replace(" m", "").replace(",", ".")
        tool_width_old = tool.width.replace(" m", "").replace(",", ".")
        tool_height_old = tool.height.replace(" m", "").replace(",", ".")
        tool_length_old = tool.length.replace(" m", "").replace(",", ".")

    fct = FCT.query.filter_by(alttechnologie='N').order_by(FCT.position).all()
    techs = Technology.query.filter_by(alttechnologie='N').order_by(Technology.position).all()
    alttech = Technology.query.filter_by(alttechnologie='Y').order_by(Technology.position).all()
    produktanforderung_rauheit = tool.roughness.replace(" µm", "").replace(",",".")
    produktanforderung_durchmesser = tool.diameter.replace(" m", "").replace(",", ".")
    produktanforderung_laenge = tool.length.replace(" m", "").replace(",", ".")
    produktanforderung_hoehe = tool.height.replace(" m", "").replace(",", ".")
    produktanforderung_breite = tool.width.replace(" m", "").replace(",", ".")
    breite = ''
    rauheit = ''
    hoehe = ''
    durchmesser = ''
    laenge = ''

    for i in range(1, FCT.query.filter_by(alttechnologie='N').count()+1):
        fctn = FCT.query.filter_by(position=''+str(i)).first()
        if not fctn.breite == '':
            breite = round(float(str(fctn.breite).replace(",",".")),2)

        if not fctn.laenge == '':
            laenge = round(float(str(fctn.laenge).replace(",",".")),2)

        if not fctn.hoehe == '':
            hoehe = round(float(str(fctn.hoehe).replace(",",".")),2)

        if not fctn.rauheit == '':
            rauheit = round(float(str(fctn.rauheit).replace(",",".")),2)

        if not fctn.durchmesser == '':
            durchmesser = round(float(str(fctn.durchmesser).replace(",",".")),2)
    print(rauheit)
    print(produktanforderung_rauheit)

#-----------------------------------------------------------------------------------------------
    if not rauheit == float(produktanforderung_rauheit):
        x = 1
        j = 1
        for i in range(FCT.query.filter_by(alttechnologie='N').count() + 0, 0, -1):  #von oben runter zählen
            fctn = FCT.query.filter_by(position='' + str(i)).first()
            alttechs = Technology.query.filter_by(verknüpfung=fctn.id).all()

            if not fctn.rauheit == '' and j == 1 and x == 0:

                rauheit = str(round(float(str(fctn.rauheit).replace(",",".")) - (float(tool_roghness_old) - float(produktanforderung_rauheit)),2))
                fctn.rauheit = rauheit.replace(".",",")
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.rauheit = rauheit.replace(".", ",")


                db.session.commit()
            if fctn.rauheit_ein == "":
                j = 0

                db.session.commit()
            if not fctn.rauheit == '' and  x == 1: # x ist ein Schalter, sodass immer direkt das erste Merkmal geändert wird und nicht die weiteren danach

                fctn.rauheit = produktanforderung_rauheit
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.rauheit = produktanforderung_rauheit
                db.session.commit()
                x = 0

    if not durchmesser == float(produktanforderung_durchmesser):
        x = 1
        j = 1
        for i in range(FCT.query.filter_by(alttechnologie='N').count() + 0, 0, -1):  #von oben runter zählen
            fctn = FCT.query.filter_by(position='' + str(i)).first()
            alttechs = Technology.query.filter_by(verknüpfung=fctn.id).all()
            if not fctn.durchmesser == '' and j == 1 and x == 0:

                durchmesser = str(round(float(str(fctn.durchmesser).replace(",",".")) - (float(tool_diameter_old) - float(produktanforderung_durchmesser)),2))
                fctn.durchmesser = durchmesser.replace(".",",")
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.durchmesser = durchmesser.replace(".", ",")
                db.session.commit()
            if fctn.durchmesser_ein == "":
                j = 0

                db.session.commit()
            if not fctn.durchmesser == '' and  x == 1: # x ist ein Schalter, sodass immer direkt das erste Merkmal geändert wird und nicht die weiteren danach
                #flash("Bitte" + fctn.name + "überprüfen!")
                fctn.durchmesser = produktanforderung_durchmesser
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.durchmesser = produktanforderung_durchmesser
                db.session.commit()
                x = 0

    if not hoehe == float(produktanforderung_hoehe):
        x = 1
        j = 1
        for i in range(FCT.query.filter_by(alttechnologie='N').count() + 0, 0, -1):  #von oben runter zählen
            fctn = FCT.query.filter_by(position='' + str(i)).first()
            alttechs = Technology.query.filter_by(verknüpfung=fctn.id).all()
            if not fctn.hoehe == '' and j == 1 and x == 0:

                hoehe = str(round(float(str(fctn.hoehe).replace(",",".")) - (float(tool_height_old) - float(produktanforderung_hoehe)),2))
                fctn.hoehe = hoehe.replace(".",",")
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.hoehe = hoehe.replace(".", ",")
                db.session.commit()
            if fctn.hoehe_ein == "":
                j = 0

                db.session.commit()
            if not fctn.hoehe == '' and  x == 1: # x ist ein Schalter, sodass immer direkt das erste Merkmal geändert wird und nicht die weiteren danach
                #flash("Bitte" + fctn.name + "überprüfen!")
                fctn.hoehe = produktanforderung_hoehe
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.hoehe = produktanforderung_hoehe
                db.session.commit()
                x = 0

    if not breite == float(produktanforderung_breite):
        x = 1
        j = 1
        for i in range(FCT.query.filter_by(alttechnologie='N').count() + 0, 0, -1):  #von oben runter zählen
            fctn = FCT.query.filter_by(position='' + str(i)).first()
            alttechs = Technology.query.filter_by(verknüpfung=fctn.id).all()
            if not fctn.breite == '' and j == 1 and x == 0:

                breite = str(round(float(str(fctn.breite).replace(",",".")) - (float(tool_width_old) - float(produktanforderung_breite)),2))
                fctn.breite = breite.replace(".",",")
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.breite = breite.replace(".", ",")
                db.session.commit()
            if fctn.breite_ein == "":
                j = 0

                db.session.commit()
            if not fctn.breite == '' and  x == 1: # x ist ein Schalter, sodass immer direkt das erste Merkmal geändert wird und nicht die weiteren danach
                #flash("Bitte" + fctn.name + "überprüfen!")
                fctn.breite = produktanforderung_breite
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.breite = produktanforderung_breite
                db.session.commit()
                x = 0

    if not laenge == float(produktanforderung_laenge):
        x = 1
        j = 1
        for i in range(FCT.query.filter_by(alttechnologie='N').count() + 0, 0, -1):  #von oben runter zählen
            fctn = FCT.query.filter_by(position='' + str(i)).first()
            alttechs = Technology.query.filter_by(verknüpfung=fctn.id).all()
            if not fctn.laenge == '' and j == 1 and x == 0:

                laenge = str(round(float(str(fctn.laenge).replace(",",".")) - (float(tool_length_old) - float(produktanforderung_laenge)),2))
                fctn.laenge = laenge.replace(".",",")
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.laenge = laenge.replace(".", ",")
                db.session.commit()
            if fctn.laenge_ein == "":
                j = 0

                db.session.commit()
            if not fctn.laenge == '' and  x == 1: # x ist ein Schalter, sodass immer direkt das erste Merkmal geändert wird und nicht die weiteren danach
                #flash("Bitte" + fctn.name + "überprüfen!")
                fctn.laenge = produktanforderung_laenge
                for z in alttechs:
                    fct_alttech = FCT.query.get_or_404(z.id)
                    fct_alttech.laenge = produktanforderung_laenge
                db.session.commit()
                x = 0

#------------------FCT-Table aktualisieren--------------------------------------------------------
    for i in range(1, FCT.query.filter_by(alttechnologie='N').count()+1):
        fctn = FCT.query.filter_by(position=''+str(i)).first()
        if not fctn.breite == '':
            breite = fctn.breite

        if not fctn.laenge == '':
            laenge = fctn.laenge

        if not fctn.hoehe == '':
            hoehe = fctn.hoehe

        if not fctn.rauheit == '':
            rauheit = fctn.rauheit

        if not fctn.durchmesser == '':
            durchmesser = fctn.durchmesser
#-----------------------------------------------------------------------------
    for k in range(1, FCT.query.filter_by(alttechnologie='N').count()+1):
        fctx = FCT.query.filter_by(position=''+str(k)).first()
        if fctx.position > 1:
            fctx_before = FCT.query.filter_by(position=''+str(k-1)).first()
            fctx.rauheit_ein = fctx_before.rauheit

            fctx.durchmesser_ein = fctx_before.durchmesser
            fctx.hoehe_ein = fctx_before.hoehe
            fctx.breite_ein = fctx_before.breite
            fctx.laenge_ein = fctx_before.laenge

            db.session.commit()
#-----------------------------------------------------------------------------

    for j in range(1, FCT.query.count()+1):

        fct2 = FCT.query.get_or_404(j)
        if not fct2.rauheit == "":
            rauheit_bauteil = float(str(fct2.rauheit).replace(",", "."))
        if not fct2.breite == "":
            breite_bauteil = float(str(fct2.breite).replace(",", "."))
        if not fct2.hoehe == "":
            hoehe_bauteil = float(str(fct2.hoehe).replace(",", "."))
        if not fct2.laenge == "":
            laenge_bauteil = float(str(fct2.laenge).replace(",", "."))
        if not fct2.durchmesser == "":
            durchmesser_bauteil = float(str(fct2.durchmesser).replace(",", "."))

        ft = Technology.query.get_or_404(j)
        rauheit_a = float(str(ft.roughness_a).replace(",", "."))
        rauheit_b = float(str(ft.roughness_b).replace(",", "."))
        rauheit_c = float(str(ft.roughness_c).replace(",", "."))
        rauheit_d = float(str(ft.roughness_d).replace(",", "."))
        maxbearbeitungswegx_a = float(str(ft.max_machining_path_x_a).replace(",", "."))
        maxbearbeitungswegx_b = float(str(ft.max_machining_path_x_b).replace(",", "."))
        maxbearbeitungswegx_c = float(str(ft.max_machining_path_x_c).replace(",", "."))
        maxbearbeitungswegx_d = float(str(ft.max_machining_path_x_d).replace(",", "."))
        maxbearbeitungswegy_a = float(str(ft.max_machining_path_y_a).replace(",", "."))
        maxbearbeitungswegy_b = float(str(ft.max_machining_path_y_b).replace(",", "."))
        maxbearbeitungswegy_c = float(str(ft.max_machining_path_y_c).replace(",", "."))
        maxbearbeitungswegy_d = float(str(ft.max_machining_path_y_d).replace(",", "."))
        maxbearbeitungswegz_a = float(str(ft.max_machining_path_z_a).replace(",", "."))
        maxbearbeitungswegz_b = float(str(ft.max_machining_path_z_b).replace(",", "."))
        maxbearbeitungswegz_c = float(str(ft.max_machining_path_z_c).replace(",", "."))
        maxbearbeitungswegz_d = float(str(ft.max_machining_path_z_d).replace(",", "."))
        formtoleranz_a = float(str(ft.shape_tolerance_a).replace(",", "."))
        formtoleranz_b = float(str(ft.shape_tolerance_b).replace(",", "."))
        formtoleranz_c = float(str(ft.shape_tolerance_c).replace(",", "."))
        formtoleranz_d = float(str(ft.shape_tolerance_d).replace(",", "."))

        fähigkeit_laenge = ''
        fähigkeit_breite = ''
        fähigkeit_hoehe = ''
        fähigkeit_rauheit = ''
        fähigkeit_durchmesser = ''

        if not fct2.laenge == '':
            if maxbearbeitungswegx_b <= laenge_bauteil <= maxbearbeitungswegx_c:
                fähigkeit_laenge = '2'
            if maxbearbeitungswegx_a <= laenge_bauteil < maxbearbeitungswegx_b or maxbearbeitungswegx_c <= laenge_bauteil < maxbearbeitungswegx_d:
                fähigkeit_laenge = '1'
            if maxbearbeitungswegx_a > laenge_bauteil or maxbearbeitungswegx_d < laenge_bauteil:
                fähigkeit_laenge = '0'

        if not fct2.breite == '':
            if maxbearbeitungswegy_b <= breite_bauteil <= maxbearbeitungswegy_c:
                fähigkeit_breite = '2'
            if maxbearbeitungswegy_a <= breite_bauteil < maxbearbeitungswegy_b or maxbearbeitungswegy_c <= breite_bauteil < maxbearbeitungswegy_d:
                fähigkeit_breite = '1'
            if maxbearbeitungswegy_a > breite_bauteil or maxbearbeitungswegy_d < breite_bauteil:
                fähigkeit_breite = '0'

        if not fct2.hoehe == '':
            if maxbearbeitungswegz_b <= hoehe_bauteil <= maxbearbeitungswegz_c:
                fähigkeit_hoehe = '2'
            if maxbearbeitungswegz_a <= hoehe_bauteil < maxbearbeitungswegz_b or maxbearbeitungswegz_c <= hoehe_bauteil < maxbearbeitungswegz_d:
                fähigkeit_hoehe = '1'
            if maxbearbeitungswegz_a > hoehe_bauteil or maxbearbeitungswegz_d < hoehe_bauteil:
                fähigkeit_hoehe = '0'

        if not fct2.rauheit == '':
            if rauheit_b <= rauheit_bauteil <= rauheit_c:
                fähigkeit_rauheit = '2'
            if rauheit_a <= rauheit_bauteil < rauheit_b or rauheit_c <= rauheit_bauteil < rauheit_d:
                fähigkeit_rauheit = '1'
            if rauheit_a > rauheit_bauteil or rauheit_d < rauheit_bauteil:
                fähigkeit_rauheit = '0'

        if not fct2.durchmesser == '':
            if formtoleranz_b <= durchmesser_bauteil <= formtoleranz_c:
                fähigkeit_durchmesser = '2'
            if formtoleranz_a <= durchmesser_bauteil < formtoleranz_b or formtoleranz_c <= durchmesser_bauteil < formtoleranz_d:
                fähigkeit_durchmesser = '1'
            if formtoleranz_a > durchmesser_bauteil or formtoleranz_d < durchmesser_bauteil:
                fähigkeit_durchmesser = '0'

        if fähigkeit_laenge == '2' or fähigkeit_hoehe == '2' or fähigkeit_breite == '2' or fähigkeit_rauheit == '2' or fähigkeit_durchmesser == '2':
            ft.capability = '2'
        if fähigkeit_laenge == '1' or fähigkeit_hoehe == '1' or fähigkeit_breite == '1' or fähigkeit_rauheit == '1' or fähigkeit_durchmesser == '1':
            ft.capability = '1'
        if fähigkeit_laenge == '0' or fähigkeit_hoehe == '0' or fähigkeit_breite == '0' or fähigkeit_rauheit == '0' or fähigkeit_durchmesser == '0':
            ft.capability = '0'

        db.session.commit()

    return render_template(
        "main/ft.html",technology = technology, tool=tool, techs=techs, alttech=alttech, fct = fct, breite = breite, rauheit = rauheit, durchmesser = durchmesser, hoehe = hoehe, laenge = laenge)

def readData():

    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    cursor_dat = c.execute("SELECT * FROM data2")

    data = cursor_dat.fetchall()

    cursor_col = c.execute("PRAGMA table_info(data2)")

    columns = cursor_col.fetchall()

    conn.close()

    return data, columns


def processData(request):
    file = request.files["file"]
    print(file)
    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    # init data frame
    df = pd.read_excel(file, header=1, usecols="B:ZZZZZ")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # extract header and types
    header = df.columns.values.tolist()
    units = []
    for i, _ in enumerate(header):
        name = header[i]
        h = name
        u = "Text"
        if " : " in name:
            ind = name.index(" : ")
            h = name[0:ind]
            u = name[ind + 3: len(name)]
        header[i] = h
        units.append(u)
    df.columns = header
    units = pd.DataFrame(units, columns=["Units"])

    # update data and unit table
    c.execute("DROP TABLE IF EXISTS data2;")
    c.execute("DROP TABLE IF EXISTS unit;")

    df.to_sql(
        "data2",
        conn,
        schema=None,
        if_exists="fail",
        index=True,
        index_label=None,
        chunksize=None,
        dtype=None,
        method=None,
    )
    units.to_sql(
        "unit",
        conn,
        schema=None,
        if_exists="fail",
        index=True,
        index_label=None,
        chunksize=None,
        dtype=None,
        method=None,
    )

    # commit changes and close db connection
    conn.commit()
    conn.close()

    conn = sqlite3.connect("app.db")
    data = pd.read_sql_query("SELECT * FROM data2 ORDER BY ROWID ASC", conn)
    column_names = data.columns.tolist()

    conn.close()


#
# CRUD: Hier sind die CREATE, READ, UPDATE und DELETE Methoden
#

# Model Technology


@main.route('/create_technology', methods=["GET", "POST"])
def create_technology():
    if request.method == 'POST':
        position = request.form['position']
        name = request.form['c00']
        max_machining_path_x_a = request.form['c11']
        max_machining_path_x_b = request.form['c12']
        max_machining_path_x_c = request.form['c13']
        max_machining_path_x_d = request.form['c14']
        max_machining_path_y_a = request.form['c21']
        max_machining_path_y_b = request.form['c22']
        max_machining_path_y_c = request.form['c23']
        max_machining_path_y_d = request.form['c24']
        max_machining_path_z_a = request.form['c31']
        max_machining_path_z_b = request.form['c32']
        max_machining_path_z_c = request.form['c33']
        max_machining_path_z_d = request.form['c34']
        shape_tolerance_a = request.form['c41']
        shape_tolerance_b = request.form['c42']
        shape_tolerance_c = request.form['c43']
        shape_tolerance_d = request.form['c44']
        roughness_a = request.form['c51']
        roughness_b = request.form['c52']
        roughness_c = request.form['c53']
        roughness_d = request.form['c54']
        alttechnologie = 'N'
        verknüpfung = 'N'
        capability = '0'
        new = Technology(position = position, name = name, roughness_a = roughness_a, roughness_b = roughness_b, roughness_c = roughness_c, roughness_d = roughness_d, shape_tolerance_a = shape_tolerance_a, shape_tolerance_b = shape_tolerance_b, shape_tolerance_c = shape_tolerance_c, shape_tolerance_d = shape_tolerance_d, max_machining_path_x_a = max_machining_path_x_a, max_machining_path_x_b = max_machining_path_x_b, max_machining_path_x_c = max_machining_path_x_c, max_machining_path_x_d = max_machining_path_x_d, max_machining_path_y_a = max_machining_path_y_a, max_machining_path_y_b = max_machining_path_y_b, max_machining_path_y_c = max_machining_path_y_c, max_machining_path_y_d = max_machining_path_y_d, max_machining_path_z_a = max_machining_path_z_a, max_machining_path_z_b = max_machining_path_z_b, max_machining_path_z_c =max_machining_path_z_c, max_machining_path_z_d = max_machining_path_z_d, alttechnologie = alttechnologie, verknüpfung = verknüpfung,capability = capability)
        db.session.add(new)

        position = request.form['position']
        name = request.form['c00']
        laenge = request.form['check1']
        breite = request.form['check2']
        hoehe = request.form['check3']
        rauheit = request.form['check4']
        durchmesser = request.form['check5']
        laenge_ein = request.form['input1']
        breite_ein = request.form['input2']
        hoehe_ein = request.form['input3']
        rauheit_ein = request.form['input4']
        durchmesser_ein = request.form['input5']
        alttechnologie = 'N'
        db.session.add(FCT(position=position, name=name, breite=breite, hoehe=hoehe, laenge=laenge, rauheit=rauheit,
                           durchmesser=durchmesser, alttechnologie=alttechnologie, laenge_ein = laenge_ein, breite_ein = breite_ein, hoehe_ein = hoehe_ein, rauheit_ein = rauheit_ein, durchmesser_ein = durchmesser_ein ))

        db.session.commit()

        fct = FCT.query.order_by(FCT.id.desc()).first()
        if not fct.rauheit == '':
            rauheit_bauteil = float(str(fct.rauheit).replace(",", "."))
        if not fct.breite == '':
            breite_bauteil = float(str(fct.breite).replace(",", "."))
        if not fct.hoehe == '':
            hoehe_bauteil = float(str(fct.hoehe).replace(",", "."))
        if not fct.laenge == '':
            laenge_bauteil = float(str(fct.laenge).replace(",", "."))
        if not fct.durchmesser == '':
            durchmesser_bauteil = float(str(fct.durchmesser).replace(",", "."))

        ft = Technology.query.order_by(Technology.id.desc()).first()
        rauheit_a = float(str(ft.roughness_a).replace(",", "."))
        rauheit_b = float(str(ft.roughness_b).replace(",", "."))
        rauheit_c = float(str(ft.roughness_c).replace(",", "."))
        rauheit_d = float(str(ft.roughness_d).replace(",", "."))
        maxbearbeitungswegx_a = float(str(ft.max_machining_path_x_a).replace(",", "."))
        maxbearbeitungswegx_b = float(str(ft.max_machining_path_x_b).replace(",", "."))
        maxbearbeitungswegx_c = float(str(ft.max_machining_path_x_c).replace(",", "."))
        maxbearbeitungswegx_d = float(str(ft.max_machining_path_x_d).replace(",", "."))
        maxbearbeitungswegy_a = float(str(ft.max_machining_path_y_a).replace(",", "."))
        maxbearbeitungswegy_b = float(str(ft.max_machining_path_y_b).replace(",", "."))
        maxbearbeitungswegy_c = float(str(ft.max_machining_path_y_c).replace(",", "."))
        maxbearbeitungswegy_d = float(str(ft.max_machining_path_y_d).replace(",", "."))
        maxbearbeitungswegz_a = float(str(ft.max_machining_path_z_a).replace(",", "."))
        maxbearbeitungswegz_b = float(str(ft.max_machining_path_z_b).replace(",", "."))
        maxbearbeitungswegz_c = float(str(ft.max_machining_path_z_c).replace(",", "."))
        maxbearbeitungswegz_d = float(str(ft.max_machining_path_z_d).replace(",", "."))
        formtoleranz_a = float(str(ft.shape_tolerance_a).replace(",", "."))
        formtoleranz_b = float(str(ft.shape_tolerance_b).replace(",", "."))
        formtoleranz_c = float(str(ft.shape_tolerance_c).replace(",", "."))
        formtoleranz_d = float(str(ft.shape_tolerance_d).replace(",", "."))

        fähigkeit_laenge = ''
        fähigkeit_breite = ''
        fähigkeit_hoehe = ''
        fähigkeit_rauheit = ''
        fähigkeit_durchmesser = ''

        if not laenge == '':
            if maxbearbeitungswegx_b <= laenge_bauteil <= maxbearbeitungswegx_c:
                fähigkeit_laenge = '2'
            if maxbearbeitungswegx_a <= laenge_bauteil < maxbearbeitungswegx_b or maxbearbeitungswegx_c <= laenge_bauteil < maxbearbeitungswegx_d:
                fähigkeit_laenge = '1'
            if maxbearbeitungswegx_a > laenge_bauteil or maxbearbeitungswegx_d < laenge_bauteil:
                fähigkeit_laenge = '0'

        if not breite == '':
            if maxbearbeitungswegy_b <= breite_bauteil <= maxbearbeitungswegy_c:
                fähigkeit_breite = '2'
            if maxbearbeitungswegy_a <= breite_bauteil < maxbearbeitungswegy_b or maxbearbeitungswegy_c <= breite_bauteil < maxbearbeitungswegy_d:
                fähigkeit_breite = '1'
            if maxbearbeitungswegy_a > breite_bauteil or maxbearbeitungswegy_d < breite_bauteil:
                fähigkeit_breite = '0'

        if not hoehe == '':
            if maxbearbeitungswegz_b <= hoehe_bauteil <= maxbearbeitungswegz_c:
                fähigkeit_hoehe = '2'
            if maxbearbeitungswegz_a <= hoehe_bauteil < maxbearbeitungswegz_b or maxbearbeitungswegz_c <= hoehe_bauteil < maxbearbeitungswegz_d:
                fähigkeit_hoehe = '1'
            if maxbearbeitungswegz_a > hoehe_bauteil or maxbearbeitungswegz_d < hoehe_bauteil:
                fähigkeit_hoehe = '0'

        if not rauheit == '':
            if rauheit_b <= rauheit_bauteil <= rauheit_c:
                fähigkeit_rauheit = '2'
            if rauheit_a <= rauheit_bauteil < rauheit_b or rauheit_c <= rauheit_bauteil < rauheit_d:
                fähigkeit_rauheit = '1'
            if rauheit_a > rauheit_bauteil or rauheit_d < rauheit_bauteil:
                fähigkeit_rauheit = '0'

        if not durchmesser == '':
            if formtoleranz_b <= durchmesser_bauteil <= formtoleranz_c:
                fähigkeit_durchmesser = '2'
            if formtoleranz_a <= durchmesser_bauteil < formtoleranz_b or formtoleranz_c <= durchmesser_bauteil < formtoleranz_d:
                fähigkeit_durchmesser = '1'
            if formtoleranz_a > durchmesser_bauteil or formtoleranz_d < durchmesser_bauteil:
                fähigkeit_durchmesser = '0'

        if fähigkeit_laenge == '2' or fähigkeit_hoehe == '2' or fähigkeit_breite == '2' or fähigkeit_rauheit == '2' or fähigkeit_durchmesser == '2':
            ft.capability = '2'
        if fähigkeit_laenge == '1' or fähigkeit_hoehe == '1' or fähigkeit_breite == '1' or fähigkeit_rauheit == '1' or fähigkeit_durchmesser == '1':
            ft.capability = '1'
        if fähigkeit_laenge == '0' or fähigkeit_hoehe == '0' or fähigkeit_breite == '0' or fähigkeit_rauheit == '0' or fähigkeit_durchmesser == '0':
            ft.capability = '0'

        db.session.commit()

        if Tool.query.count() == 2:  # gibt es noch einen zweiten eintrag?
            delete_entry = Tool.query.get_or_404(2)
            db.session.delete(delete_entry)
            db.session.commit()
        return redirect('/main/ft', )

    return render_template("main/create_technology.html")

@main.route('/create_alttechnology', methods=["GET", "POST"])
def create_alttechnology():
    if request.method == 'POST':
        position = ''
        name = request.form['ca00']
        max_machining_path_x_a = request.form['ca11']
        max_machining_path_x_b = request.form['ca12']
        max_machining_path_x_c = request.form['ca13']
        max_machining_path_x_d = request.form['ca14']
        max_machining_path_y_a = request.form['ca21']
        max_machining_path_y_b = request.form['ca22']
        max_machining_path_y_c = request.form['ca23']
        max_machining_path_y_d = request.form['ca24']
        max_machining_path_z_a = request.form['ca31']
        max_machining_path_z_b = request.form['ca32']
        max_machining_path_z_c = request.form['ca33']
        max_machining_path_z_d = request.form['ca34']
        shape_tolerance_a = request.form['ca41']
        shape_tolerance_b = request.form['ca42']
        shape_tolerance_c = request.form['ca43']
        shape_tolerance_d = request.form['ca44']
        roughness_a = request.form['ca51']
        roughness_b = request.form['ca52']
        roughness_c = request.form['ca53']
        roughness_d = request.form['ca54']
        alttechnologie = 'Y'
        verknüpfung = request.form['altft']
        capability = '0'
        new = Technology(position = position, name = name, roughness_a = roughness_a, roughness_b = roughness_b, roughness_c = roughness_c, roughness_d = roughness_d, shape_tolerance_a = shape_tolerance_a, shape_tolerance_b = shape_tolerance_b, shape_tolerance_c = shape_tolerance_c, shape_tolerance_d = shape_tolerance_d, max_machining_path_x_a = max_machining_path_x_a, max_machining_path_x_b = max_machining_path_x_b, max_machining_path_x_c = max_machining_path_x_c, max_machining_path_x_d = max_machining_path_x_d, max_machining_path_y_a = max_machining_path_y_a, max_machining_path_y_b = max_machining_path_y_b, max_machining_path_y_c = max_machining_path_y_c, max_machining_path_y_d = max_machining_path_y_d, max_machining_path_z_a = max_machining_path_z_a, max_machining_path_z_b = max_machining_path_z_b, max_machining_path_z_c =max_machining_path_z_c, max_machining_path_z_d = max_machining_path_z_d, alttechnologie = alttechnologie, verknüpfung = verknüpfung,capability = capability)
        db.session.add(new)

        position = ''
        name = request.form['ca00']
        laenge = request.form['check1']
        breite = request.form['check2']
        hoehe = request.form['check3']
        rauheit = request.form['check4']
        durchmesser = request.form['check5']
        laenge_ein = request.form['input1']
        breite_ein = request.form['input2']
        hoehe_ein = request.form['input3']
        rauheit_ein = request.form['input4']
        durchmesser_ein = request.form['input5']
        alttechnologie = 'Y'
        db.session.add(FCT(position=position, name=name, breite=breite, hoehe=hoehe, laenge=laenge, rauheit=rauheit,
                           durchmesser=durchmesser, alttechnologie=alttechnologie, laenge_ein = laenge_ein, breite_ein = breite_ein, hoehe_ein = hoehe_ein, rauheit_ein = rauheit_ein, durchmesser_ein = durchmesser_ein))

        db.session.commit()

        fct = FCT.query.order_by(FCT.id.desc()).first()
        if not fct.rauheit == '':
            rauheit_bauteil = float(str(fct.rauheit).replace(",", "."))
        if not fct.breite == '':
            breite_bauteil = float(str(fct.breite).replace(",", "."))
        if not fct.hoehe == '':
            hoehe_bauteil = float(str(fct.hoehe).replace(",", "."))
        if not fct.laenge == '':
            laenge_bauteil = float(str(fct.laenge).replace(",", "."))
        if not fct.durchmesser == '':
            durchmesser_bauteil = float(str(fct.durchmesser).replace(",", "."))

        ft = Technology.query.order_by(Technology.id.desc()).first()
        rauheit_a = float(str(ft.roughness_a).replace(",", "."))
        rauheit_b = float(str(ft.roughness_b).replace(",", "."))
        rauheit_c = float(str(ft.roughness_c).replace(",", "."))
        rauheit_d = float(str(ft.roughness_d).replace(",", "."))
        maxbearbeitungswegx_a = float(str(ft.max_machining_path_x_a).replace(",", "."))
        maxbearbeitungswegx_b = float(str(ft.max_machining_path_x_b).replace(",", "."))
        maxbearbeitungswegx_c = float(str(ft.max_machining_path_x_c).replace(",", "."))
        maxbearbeitungswegx_d = float(str(ft.max_machining_path_x_d).replace(",", "."))
        maxbearbeitungswegy_a = float(str(ft.max_machining_path_y_a).replace(",", "."))
        maxbearbeitungswegy_b = float(str(ft.max_machining_path_y_b).replace(",", "."))
        maxbearbeitungswegy_c = float(str(ft.max_machining_path_y_c).replace(",", "."))
        maxbearbeitungswegy_d = float(str(ft.max_machining_path_y_d).replace(",", "."))
        maxbearbeitungswegz_a = float(str(ft.max_machining_path_z_a).replace(",", "."))
        maxbearbeitungswegz_b = float(str(ft.max_machining_path_z_b).replace(",", "."))
        maxbearbeitungswegz_c = float(str(ft.max_machining_path_z_c).replace(",", "."))
        maxbearbeitungswegz_d = float(str(ft.max_machining_path_z_d).replace(",", "."))
        formtoleranz_a = float(str(ft.shape_tolerance_a).replace(",", "."))
        formtoleranz_b = float(str(ft.shape_tolerance_b).replace(",", "."))
        formtoleranz_c = float(str(ft.shape_tolerance_c).replace(",", "."))
        formtoleranz_d = float(str(ft.shape_tolerance_d).replace(",", "."))

        fähigkeit_laenge = ''
        fähigkeit_breite = ''
        fähigkeit_hoehe = ''
        fähigkeit_rauheit = ''
        fähigkeit_durchmesser = ''

        if not laenge == '':
            if maxbearbeitungswegx_b <= laenge_bauteil <= maxbearbeitungswegx_c:
                fähigkeit_laenge = '2'
            if maxbearbeitungswegx_a <= laenge_bauteil < maxbearbeitungswegx_b or maxbearbeitungswegx_c <= laenge_bauteil < maxbearbeitungswegx_d:
                fähigkeit_laenge = '1'
            if maxbearbeitungswegx_a > laenge_bauteil or maxbearbeitungswegx_d < laenge_bauteil:
                fähigkeit_laenge = '0'

        if not breite == '':
            if maxbearbeitungswegy_b <= breite_bauteil <= maxbearbeitungswegy_c:
                fähigkeit_breite = '2'
            if maxbearbeitungswegy_a <= breite_bauteil < maxbearbeitungswegy_b or maxbearbeitungswegy_c <= breite_bauteil < maxbearbeitungswegy_d:
                fähigkeit_breite = '1'
            if maxbearbeitungswegy_a > breite_bauteil or maxbearbeitungswegy_d < breite_bauteil:
                fähigkeit_breite = '0'

        if not hoehe == '':
            if maxbearbeitungswegz_b <= hoehe_bauteil <= maxbearbeitungswegz_c:
                fähigkeit_hoehe = '2'
            if maxbearbeitungswegz_a <= hoehe_bauteil < maxbearbeitungswegz_b or maxbearbeitungswegz_c <= hoehe_bauteil < maxbearbeitungswegz_d:
                fähigkeit_hoehe = '1'
            if maxbearbeitungswegz_a > hoehe_bauteil or maxbearbeitungswegz_d < hoehe_bauteil:
                fähigkeit_hoehe = '0'

        if not rauheit == '':
            if rauheit_b <= rauheit_bauteil <= rauheit_c:
                fähigkeit_rauheit = '2'
            if rauheit_a <= rauheit_bauteil < rauheit_b or rauheit_c <= rauheit_bauteil < rauheit_d:
                fähigkeit_rauheit = '1'
            if rauheit_a > rauheit_bauteil or rauheit_d < rauheit_bauteil:
                fähigkeit_rauheit = '0'

        if not durchmesser == '':
            if formtoleranz_b <= durchmesser_bauteil <= formtoleranz_c:
                fähigkeit_durchmesser = '2'
            if formtoleranz_a <= durchmesser_bauteil < formtoleranz_b or formtoleranz_c <= durchmesser_bauteil < formtoleranz_d:
                fähigkeit_durchmesser = '1'
            if formtoleranz_a > durchmesser_bauteil or formtoleranz_d < durchmesser_bauteil:
                fähigkeit_durchmesser = '0'

        if fähigkeit_laenge == '2' or fähigkeit_hoehe == '2' or fähigkeit_breite == '2' or fähigkeit_rauheit == '2' or fähigkeit_durchmesser == '2':
            ft.capability = '2'
        if fähigkeit_laenge == '1' or fähigkeit_hoehe == '1' or fähigkeit_breite == '1' or fähigkeit_rauheit == '1' or fähigkeit_durchmesser == '1':
            ft.capability = '1'
        if fähigkeit_laenge == '0' or fähigkeit_hoehe == '0' or fähigkeit_breite == '0' or fähigkeit_rauheit == '0' or fähigkeit_durchmesser == '0':
            ft.capability = '0'

        db.session.commit()

        if Tool.query.count() == 2:  # gibt es noch einen zweiten eintrag?
            delete_entry = Tool.query.get_or_404(2)
            db.session.delete(delete_entry)
            db.session.commit()
        return redirect('/main/ft', )
    technology = Technology.query.order_by(Technology.position).all()
    return render_template("main/create_alttechnology.html", technology = technology)

@main.route('/update_technology/<int:id>', methods=['GET', 'POST'])
def update_technology(id):
    """
    READ oder UPDATE Technology

    tech = Technology.query.get_or_404(id)
    form = TechnologyForm(obj=tech)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(tech)
            db.session.commit()
            return redirect(url_for('main.index'))
        flash("Validierung fehlgeschlagen")
    return render_template('main/update_technology.html', form=form, tech=tech)
"""
    technologie = Technology.query.get_or_404(id)
    fct = FCT.query.get_or_404(id)
    if request.method == 'POST':

        technologie.name = request.form['cb00']
        technologie.max_machining_path_x_a = request.form['cb11']
        technologie.max_machining_path_x_b = request.form['cb12']
        technologie.max_machining_path_x_c = request.form['cb13']
        technologie.max_machining_path_x_d = request.form['cb14']
        technologie.max_machining_path_y_a = request.form['cb21']
        technologie.max_machining_path_y_b = request.form['cb22']
        technologie.max_machining_path_y_c = request.form['cb23']
        technologie.max_machining_path_y_d = request.form['cb24']
        technologie.max_machining_path_z_a = request.form['cb31']
        technologie.max_machining_path_z_b = request.form['cb32']
        technologie.max_machining_path_z_c = request.form['cb33']
        technologie.max_machining_path_z_d = request.form['cb34']
        technologie.shape_tolerance_a = request.form['cb41']
        technologie.shape_tolerance_b = request.form['cb42']
        technologie.shape_tolerance_c = request.form['cb43']
        technologie.shape_tolerance_d = request.form['cb44']
        technologie.roughness_a = request.form['cb51']
        technologie.roughness_b = request.form['cb52']
        technologie.roughness_c = request.form['cb53']
        technologie.roughness_d = request.form['cb54']
        technologie.position = request.form['position1']

        fct.name = request.form['cb00']
        fct.position = request.form['position1']
        fct.laenge = request.form['check1']
        fct.breite = request.form['check2']
        fct.hoehe = request.form['check3']
        fct.rauheit = request.form['check4']
        fct.durchmesser = request.form['check5']
        technologie.capability = '0'
        db.session.commit()


        if not fct.rauheit == "":
            rauheit_bauteil = float(str(fct.rauheit).replace(",", "."))
        if not fct.breite == "":
            breite_bauteil = float(str(fct.breite).replace(",", "."))
        if not fct.hoehe == "":
            hoehe_bauteil = float(str(fct.hoehe).replace(",", "."))
        if not fct.laenge == "":
            laenge_bauteil = float(str(fct.laenge).replace(",", "."))
        if not fct.durchmesser == "":
            durchmesser_bauteil = float(str(fct.durchmesser).replace(",", "."))

        ft = Technology.query.get_or_404(id)
        rauheit_a = float(str(ft.roughness_a).replace(",", "."))
        rauheit_b = float(str(ft.roughness_b).replace(",", "."))
        rauheit_c = float(str(ft.roughness_c).replace(",", "."))
        rauheit_d = float(str(ft.roughness_d).replace(",", "."))
        maxbearbeitungswegx_a = float(str(ft.max_machining_path_x_a).replace(",", "."))
        maxbearbeitungswegx_b = float(str(ft.max_machining_path_x_b).replace(",", "."))
        maxbearbeitungswegx_c = float(str(ft.max_machining_path_x_c).replace(",", "."))
        maxbearbeitungswegx_d = float(str(ft.max_machining_path_x_d).replace(",", "."))
        maxbearbeitungswegy_a = float(str(ft.max_machining_path_y_a).replace(",", "."))
        maxbearbeitungswegy_b = float(str(ft.max_machining_path_y_b).replace(",", "."))
        maxbearbeitungswegy_c = float(str(ft.max_machining_path_y_c).replace(",", "."))
        maxbearbeitungswegy_d = float(str(ft.max_machining_path_y_d).replace(",", "."))
        maxbearbeitungswegz_a = float(str(ft.max_machining_path_z_a).replace(",", "."))
        maxbearbeitungswegz_b = float(str(ft.max_machining_path_z_b).replace(",", "."))
        maxbearbeitungswegz_c = float(str(ft.max_machining_path_z_c).replace(",", "."))
        maxbearbeitungswegz_d = float(str(ft.max_machining_path_z_d).replace(",", "."))
        formtoleranz_a = float(str(ft.shape_tolerance_a).replace(",", "."))
        formtoleranz_b = float(str(ft.shape_tolerance_b).replace(",", "."))
        formtoleranz_c = float(str(ft.shape_tolerance_c).replace(",", "."))
        formtoleranz_d = float(str(ft.shape_tolerance_d).replace(",", "."))
        laenge = fct.laenge
        breite = fct.breite
        hoehe = fct.hoehe
        rauheit = fct.rauheit
        durchmesser = fct.durchmesser

        fähigkeit_laenge = ''
        fähigkeit_breite = ''
        fähigkeit_hoehe = ''
        fähigkeit_rauheit = ''
        fähigkeit_durchmesser = ''

        if not laenge == '':
            if maxbearbeitungswegx_b <= laenge_bauteil <= maxbearbeitungswegx_c:
                fähigkeit_laenge = '2'
            if maxbearbeitungswegx_a <= laenge_bauteil < maxbearbeitungswegx_b or maxbearbeitungswegx_c <= laenge_bauteil < maxbearbeitungswegx_d:
                fähigkeit_laenge = '1'
            if maxbearbeitungswegx_a > laenge_bauteil or maxbearbeitungswegx_d < laenge_bauteil:
                fähigkeit_laenge = '0'


        if not breite == '':
            if maxbearbeitungswegy_b <= breite_bauteil <= maxbearbeitungswegy_c:
                fähigkeit_breite = '2'
            if maxbearbeitungswegy_a <= breite_bauteil < maxbearbeitungswegy_b or maxbearbeitungswegy_c <= breite_bauteil < maxbearbeitungswegy_d:
                fähigkeit_breite = '1'
            if maxbearbeitungswegy_a > breite_bauteil or maxbearbeitungswegy_d < breite_bauteil:
                fähigkeit_breite = '0'

        if not hoehe == '':
            if maxbearbeitungswegz_b <= hoehe_bauteil <= maxbearbeitungswegz_c:
                fähigkeit_hoehe = '2'
            if maxbearbeitungswegz_a <= hoehe_bauteil < maxbearbeitungswegz_b or maxbearbeitungswegz_c <= hoehe_bauteil < maxbearbeitungswegz_d:
                fähigkeit_hoehe = '1'
            if maxbearbeitungswegz_a > hoehe_bauteil or maxbearbeitungswegz_d < hoehe_bauteil:
                fähigkeit_hoehe = '0'

        if not rauheit == '':
            if rauheit_b <= rauheit_bauteil <= rauheit_c:
                fähigkeit_rauheit = '2'
            if rauheit_a <= rauheit_bauteil < rauheit_b or rauheit_c <= rauheit_bauteil < rauheit_d:
                fähigkeit_rauheit = '1'
            if rauheit_a > rauheit_bauteil or rauheit_d < rauheit_bauteil:
                fähigkeit_rauheit = '0'

        if not durchmesser == '':
            if formtoleranz_b <= durchmesser_bauteil <= formtoleranz_c:
                fähigkeit_durchmesser = '2'
            if formtoleranz_a <= durchmesser_bauteil < formtoleranz_b or formtoleranz_c <= durchmesser_bauteil < formtoleranz_d:
                fähigkeit_durchmesser = '1'
            if formtoleranz_a > durchmesser_bauteil or formtoleranz_d < durchmesser_bauteil:
                fähigkeit_durchmesser = '0'


        if fähigkeit_laenge == '2' or fähigkeit_hoehe == '2' or fähigkeit_breite == '2' or fähigkeit_rauheit == '2' or fähigkeit_durchmesser == '2':
            ft.capability = '2'
        if fähigkeit_laenge == '1' or fähigkeit_hoehe == '1' or fähigkeit_breite == '1' or fähigkeit_rauheit == '1' or fähigkeit_durchmesser == '1':
            ft.capability = '1'
        if fähigkeit_laenge == '0' or fähigkeit_hoehe == '0' or fähigkeit_breite == '0' or fähigkeit_rauheit == '0' or fähigkeit_durchmesser == '0':
            ft.capability = '0'


        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/update_technology.html',fct = fct, technologie = technologie)



@main.route('/delete_technology/<int:id>')
def delete_technology(id):
    """
    DELETE Technology
    """
    Technology.query.filter_by(id=id).delete()
    FCT.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))


# Model Tool

@main.route('/create_tool', methods=["GET", "POST"])
def create_tool():
    """
    !!TODO!!
    CREATE Tool via Excel oder händisch?
    """
    return "Create Tool Template"


@main.route('/update_tool/<int:id>', methods=['GET', 'POST'])
def update_tool(id):
    """
    READ oder UPDATE Tool
    """
    tool = Tool.query.get_or_404(id)
    #form = ToolForm(obj=tool)
    if request.method == 'POST':
#----------------------------------------------------------
        if Tool.query.count() == 2:  # gibt es noch einen zweiten eintrag?
            delete_entry = Tool.query.get_or_404(2)
            db.session.delete(delete_entry)
            db.session.commit()
        name_old = tool.name+"OLD"
        force_old = tool.force
        width_old = tool.width
        height_old = tool.height            #Damit der das Bauteil vor der Änderung noch aufrufen kann
        length_old = tool.length            # Für weitere Berechnungen
        roughness_old = tool.roughness
        diameter_old = tool.diameter
        new = Tool(name = name_old, force = force_old, width = width_old, height = height_old, length = length_old, roughness = roughness_old, diameter = diameter_old)
        db.session.add(new)
#----------------------------------------------------------
        tool.force = request.form['content1']
        tool.width = request.form['content2']
        tool.height = request.form['content3']
        tool.length = request.form['content4']
        tool.roughness = request.form['content5']
        tool.diameter = request.form['content6']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/update_tool.html', tool = tool)



@main.route('/delete_tool/<int:id>', methods=['GET', 'POST'])
def delete_tool(id):
    """
    DELETE Tool
    """
    Tool.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/position/<int:pos>', methods=['GET', 'POST'])
def position(pos):
    if request.method == 'POST':
        if float(request.form['pos'+str(pos)]) <= Technology.query.filter_by(alttechnologie='N').count():
            id = request.form['id'+str(pos)]
            technology = Technology.query.get_or_404(id)
            fct = FCT.query.get_or_404(id)
            technology.position = request.form['pos'+str(pos)]
            fct.position = request.form['pos'+str(pos)]
            technology_switch = Technology.query.filter_by(position=technology.position).first()
            fct_switch = FCT.query.filter_by(position=fct.position).first()
            technology_switch.position = pos
            fct_switch.position = pos
            db.session.commit()
        else: flash('Die maximal mögliche Anzahl an Positionen ist' +  str(Technology.query.filter_by(alttechnologie='N').count()))
        return redirect('/main/ft')



@main.route('/save', methods=['POST','GET'])
def save():
    if request.method == 'POST':

        for i in range(1,Technology.query.filter_by(alttechnologie='N').count()+1):

            id = request.form['ft'+str(i)]
            ft_neu = Technology.query.get_or_404(id)
            fct = FCT.query.get_or_404(id)
            verknüpfung = ft_neu.verknüpfung
            if not ft_neu.verknüpfung == 'N':
                fct_alt = FCT.query.get_or_404(verknüpfung)
                ft_alt = Technology.query.get_or_404(verknüpfung)
                ft_neu.alttechnologie = 'N'
                ft_neu.verknüpfung = 'N'
                ft_neu.position = ft_alt.position
                fct.position = ft_alt.position

                ft_alt.alttechnologie = 'Y'
                fct.alttechnologie = 'N'
                fct_alt.alttechnologie = 'Y'
                ft_alt.verknüpfung = ft_neu.id
                db.session.commit()

                ft_alt.position = ''
                fct_alt.position = ''
                db.session.commit()

    return redirect('/main/ft')
    #return render_template("main/ft.html")

