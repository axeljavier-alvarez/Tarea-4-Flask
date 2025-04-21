from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://usuario3:usuario3@DESKTOP-7OS5AP9/gestion_citas_medicas?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Paciente
class Paciente(db.Model):
    __tablename__ = 'Pacientes'  
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))

# Modelo de Médico
class Medico(db.Model):
    __tablename__ = 'Medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    especialidad = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))


# Modelo de Cita
class Cita(db.Model):
    __tablename__ = 'Citas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'))
    medico_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'))
    fecha_cita = db.Column(db.DateTime)
    estado = db.Column(db.String(50))
    
# Modelo de Historial Médico
class HistorialMedico(db.Model):
    __tablename__ = 'Historial_Medico'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'))
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    
    
# Ruta para listar pacientes
@app.route('/')
def index():
    pacientes = Paciente.query.all()
    return render_template('index.html', pacientes=pacientes)

# Rutas para Pacientes

@app.route('/pacientes_principal')
def pacientes_principal():
    pacientes = Paciente.query.all()
    return render_template('pacientes_principal.html', pacientes=pacientes)

@app.route('/crear_paciente', methods=['GET', 'POST'])
def crear_paciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        email = request.form['email']

        nuevo_paciente = Paciente(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento, telefono=telefono, email=email)
        db.session.add(nuevo_paciente)
        db.session.commit()

        return redirect(url_for('pacientes_principal'))

    return render_template('crear_paciente.html')

@app.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        paciente.nombre = request.form['nombre']
        paciente.apellido = request.form['apellido']
        paciente.fecha_nacimiento = request.form['fecha_nacimiento']
        paciente.telefono = request.form['telefono']
        paciente.email = request.form['email']

        db.session.commit()
        return redirect(url_for('pacientes_principal'))

    return render_template('editar_paciente.html', paciente=paciente)

@app.route('/eliminar_paciente/<int:id>', methods=['GET', 'POST'])
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(paciente)
        db.session.commit()
        return redirect(url_for('pacientes_principal'))

    return render_template('eliminar_paciente.html', paciente=paciente)

# Rutas para Médicos

@app.route('/medicos_principal')
def medicos_principal():
    medicos = Medico.query.all()
    return render_template('medicos_principal.html', medicos=medicos)

@app.route('/crear_medico', methods=['GET', 'POST'])
def crear_medico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        email = request.form['email']

        nuevo_medico = Medico(nombre=nombre, apellido=apellido, especialidad=especialidad, telefono=telefono, email=email)
        db.session.add(nuevo_medico)
        db.session.commit()

        return redirect(url_for('medicos_principal'))

    return render_template('crear_medico.html')

@app.route('/editar_medico/<int:id>', methods=['GET', 'POST'])
def editar_medico(id):
    medico = Medico.query.get_or_404(id)

    if request.method == 'POST':
        medico.nombre = request.form['nombre']
        medico.apellido = request.form['apellido']
        medico.especialidad = request.form['especialidad']
        medico.telefono = request.form['telefono']
        medico.email = request.form['email']

        db.session.commit()
        return redirect(url_for('medicos_principal'))

    return render_template('editar_medico.html', medico=medico)

@app.route('/eliminar_medico/<int:id>', methods=['GET', 'POST'])
def eliminar_medico(id):
    medico = Medico.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(medico)
        db.session.commit()
        return redirect(url_for('medicos_principal'))

    return render_template('eliminar_medico.html', medico=medico)



@app.route('/citas_principal')
def citas_principal():
    citas = Cita.query.all()
    return render_template('citas_principal.html', citas=citas)

@app.route('/crear_cita', methods=['GET', 'POST'])
def crear_cita():
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        medico_id = request.form['medico_id']
        
        fecha_cita_str = request.form['fecha_cita']
        fecha_cita = datetime.fromisoformat(fecha_cita_str)  

        estado = request.form['estado']

        nueva_cita = Cita(paciente_id=paciente_id, medico_id=medico_id, fecha_cita=fecha_cita, estado=estado)
        db.session.add(nueva_cita)
        db.session.commit()

        return redirect(url_for('citas_principal'))

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    return render_template('crear_cita.html', pacientes=pacientes, medicos=medicos)


@app.route('/editar_cita/<int:id>', methods=['GET', 'POST'])
def editar_cita(id):
    cita = Cita.query.get_or_404(id)

    if request.method == 'POST':
        cita.paciente_id = request.form['paciente_id']
        cita.medico_id = request.form['medico_id']
        
        fecha_cita_str = request.form['fecha_cita']
        cita.fecha_cita = datetime.fromisoformat(fecha_cita_str)  

        cita.estado = request.form['estado']

        db.session.commit()
        return redirect(url_for('citas_principal'))

    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    return render_template('editar_cita.html', cita=cita, pacientes=pacientes, medicos=medicos)

@app.route('/eliminar_cita/<int:id>', methods=['GET', 'POST'])
def eliminar_cita(id):
    cita = Cita.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(cita)
        db.session.commit()
        return redirect(url_for('citas_principal'))

    return render_template('eliminar_cita.html', cita=cita)



# Rutas para Historial Médico

@app.route('/historial_principal')
def historial_principal():
    historial = HistorialMedico.query.all()
    return render_template('historial_principal.html', historial=historial)

@app.route('/crear_historial', methods=['GET', 'POST'])
def crear_historial():
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        fecha_str = request.form['fecha']
        descripcion = request.form['descripcion']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        nuevo_historial = HistorialMedico(paciente_id=paciente_id, fecha=fecha, descripcion=descripcion)
        db.session.add(nuevo_historial)
        db.session.commit()

        return redirect(url_for('historial_principal'))

    pacientes = Paciente.query.all()
    return render_template('crear_historial.html', pacientes=pacientes)

@app.route('/editar_historial/<int:id>', methods=['GET', 'POST'])
def editar_historial(id):
    historial = HistorialMedico.query.get_or_404(id)

    if request.method == 'POST':
        historial.paciente_id = request.form['paciente_id']
        fecha_str = request.form['fecha']
        historial.descripcion = request.form['descripcion']

        historial.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        db.session.commit()
        return redirect(url_for('historial_principal'))

    pacientes = Paciente.query.all()
    return render_template('editar_historial.html', historial=historial, pacientes=pacientes)

@app.route('/eliminar_historial/<int:id>', methods=['GET', 'POST'])
def eliminar_historial(id):
    historial = HistorialMedico.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(historial)
        db.session.commit()
        return redirect(url_for('historial_principal'))

    return render_template('eliminar_historial.html', historial=historial)



if __name__ == '__main__':
    app.run(debug=True)