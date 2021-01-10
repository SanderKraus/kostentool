
@main.route('/produkt')
def produkt():
    data = Tool.query.first()
    return render_template('main/produktarchitektur.html', data=data)


@main.route('/system')
def system():
    technologie = Technology.query.order_by(Technology.position).all()
    ft = Technology.query.order_by(Technology.position).all()
    altft = Technology.query.filter_by(
        alttechnologie='Y').order_by(Technology.position).all()
    return render_template('main/fertigungssystem.html', technologie=technologie, ft=ft, altft=altft)


@main.route('/position/<int:id>', methods=['GET', 'POST'])
def position(id):
    technologie = Technology.query.get_or_404(id)
    if request.method == 'POST':
        technologie.position = request.form['position1']
        db.session.commit()
        return redirect('/system')
    else:
        return render_template('main/position.html', technologie=technologie)
    return ''


@main.route('/reihenfolge_fertigungssystem', methods=['GET', 'POST'])
def reihenfolge_fertigungssystem():
    technologie = Technology.query.order_by(Technology.id).all()
    if request.method == 'POST':
        for technologie in technologie:
            technologie.id = request.form[technologie.id]

            db.session.commit()

        return redirect('/system')
    else:
        return render_template('main/reihenfolge_fertigungssystem.html', technologie=technologie)
    return ''


@main.route('/ftbearbeiten/<int:id>', methods=['GET', 'POST'])
def ftbearbeiten(id):
    tech = Technology.query.get_or_404(id)
    form = TechnologyForm(obj=tech)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(tech)
            db.session.commit()
            return redirect(url_for('main.index'))
        flash("Validierung fehlgeschlagen")
    return render_template('main/ftbearbeiten.html', form=form)


@main.route('/neue_technologie', methods=['POST', 'GET'])
def neue_technologie():
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
        new = Technology(position=position, name=name, rauheit_a=rauheit_a, rauheit_b=rauheit_b, rauheit_c=rauheit_c, rauheit_d=rauheit_d, formtoleranz_a=formtoleranz_a, formtoleranz_b=formtoleranz_b, formtoleranz_c=formtoleranz_c, formtoleranz_d=formtoleranz_d, maxbearbeitungswegx_a=maxbearbeitungswegx_a, maxbearbeitungswegx_b=maxbearbeitungswegx_b, maxbearbeitungswegx_c=maxbearbeitungswegx_c, maxbearbeitungswegx_d=maxbearbeitungswegx_d,
                         maxbearbeitungswegy_a=maxbearbeitungswegy_a, maxbearbeitungswegy_b=maxbearbeitungswegy_b, maxbearbeitungswegy_c=maxbearbeitungswegy_c, maxbearbeitungswegy_d=maxbearbeitungswegy_d, maxbearbeitungswegz_a=maxbearbeitungswegz_a, maxbearbeitungswegz_b=maxbearbeitungswegz_b, maxbearbeitungswegz_c=maxbearbeitungswegz_c, maxbearbeitungswegz_d=maxbearbeitungswegz_d, alttechnologie=alttechnologie, verknüpfung=verknüpfung)

        db.session.add(new)
        db.session.commit()

        return redirect('/system',)

    return render_template("main/neue_technologie.html",)


@main.route('/neue_alttechnologie', methods=['POST', 'GET'])
def neue_alttechnologie():
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
        new = Technology(position=position, name=name, rauheit_a=rauheit_a, rauheit_b=rauheit_b, rauheit_c=rauheit_c, rauheit_d=rauheit_d, formtoleranz_a=formtoleranz_a, formtoleranz_b=formtoleranz_b, formtoleranz_c=formtoleranz_c, formtoleranz_d=formtoleranz_d, maxbearbeitungswegx_a=maxbearbeitungswegx_a, maxbearbeitungswegx_b=maxbearbeitungswegx_b, maxbearbeitungswegx_c=maxbearbeitungswegx_c, maxbearbeitungswegx_d=maxbearbeitungswegx_d,
                         maxbearbeitungswegy_a=maxbearbeitungswegy_a, maxbearbeitungswegy_b=maxbearbeitungswegy_b, maxbearbeitungswegy_c=maxbearbeitungswegy_c, maxbearbeitungswegy_d=maxbearbeitungswegy_d, maxbearbeitungswegz_a=maxbearbeitungswegz_a, maxbearbeitungswegz_b=maxbearbeitungswegz_b, maxbearbeitungswegz_c=maxbearbeitungswegz_c, maxbearbeitungswegz_d=maxbearbeitungswegz_d, alttechnologie=alttechnologie, verknüpfung=verknüpfung)

        db.session.add(new)
        db.session.commit()

        return redirect('/system',)
    technologie = Technology.query.order_by(Technology.position).all()
    return render_template("main/neue_alttechnologie.html", technologie=technologie)


@main.route('/tool')
def tool():
    data = Tool.query.first()
    Laenge = data.length  # Komma mit Punkt ersetzen
    Breite = data.width
    Hoehe = data.height

    K_F = 5000  # [€/m^3]
    K_S = 15000  # [€/m^3]
    V = Laenge * Hoehe * Breite
    return render_template('main/kostentool.html', K_F=K_F, K_S=K_S, V=V)
