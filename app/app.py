from flask import Flask, render_template, request, redirect, url_for,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/costosTalleres'
db = SQLAlchemy(app)
    
    
class Presupuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(255))
    segmento = db.Column(db.String(255))
    reparacion = db.Column(db.String(255))
    precio = db.Column(db.Float)
    fechaActualizacion = db.Column(db.String(10))
    observacion = db.Column(db.String(255))
    
    
class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15))
    vehiculo = db.Column(db.String(30))
    mensaje = db.Column(db.String(200))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    



@app.route('/')
def index():
    presupuestos = Presupuesto.query.all()
    marcas = db.session.query(Presupuesto.marca).distinct().all()
    segmentos = db.session.query(Presupuesto.segmento).distinct().all()
    reparaciones = db.session.query(Presupuesto.reparacion).distinct().all()
    comentarios = Comentario.query.order_by(Comentario.id.desc()).all()
    return render_template('index.html', presupuestos=presupuestos, marcas=marcas, segmentos=segmentos, reparaciones=reparaciones, comentarios=comentarios)

@app.route('/presupuestador')
def presupuestador():
    return render_template('presupuestador.html')

@app.route('/presupuestos', methods=['GET', 'POST'])
def presupuestos():
    presupuestos = Presupuesto.query.all()
    return render_template('presupuestos.html', presupuestos=presupuestos)

@app.route('/agregar_presupuesto')
def agregar_presupuesto():
    return render_template('agregar_presupuesto.html')

@app.route('/aniadir_presupuesto', methods=['POST'])
def aniadir_presupuesto():
    if request.method == 'POST':
        marca = request.form['marca']
        segmento = request.form['segmento']
        reparacion = request.form['reparacion']
        precio = request.form['precio']
        fechaActualizacion = request.form['fechaActualizacion']
        observacion = request.form['observacion']

        nuevo_presupuesto = Presupuesto(marca=marca, reparacion=reparacion, segmento=segmento, precio=precio, fechaActualizacion=fechaActualizacion, observacion=observacion)
        db.session.add(nuevo_presupuesto)
        db.session.commit()
        return ("Exito al agregar")
        #return render_template('confirmacion.html')


@app.route('/editar_presupuesto/<int:id>', methods=['GET', 'POST'])
def editar_presupuesto(id):
    presupuesto = Presupuesto.query.get(id)

    if request.method == 'POST':
        # Actualización del contacto según los datos del formulario
        marca_actualizado = request.form['marca']
        reparacion_actualizado = request.form['reparacion']
        segmento_actualizado = request.form['segmento']
        precio_actualizado = request.form['precio']
        fechaActualizacion_actualizado = request.form['fechaActualizacion']
        observacion_actualizado = request.form['observacion']

        # Actualizar los atributos del contacto
        presupuesto.marca = marca_actualizado
        presupuesto.segmento = segmento_actualizado
        presupuesto.reparacion = reparacion_actualizado
        presupuesto.precio = precio_actualizado
        presupuesto.fechaActualizacion = fechaActualizacion_actualizado
        presupuesto.observacion = observacion_actualizado

        db.session.commit()
        #return f'Contacto con ID {id} actualizado correctamente.'
        return ('exito')

    # Si la solicitud es GET, renderizar el formulario con los datos del contacto
    return render_template('editar_presupuesto.html', presupuesto=presupuesto)


@app.route('/seleccionar_presupuesto/<int:id>', methods=['GET', 'POST'])
def seleccionar_presupuesto(id):
    presupuesto = Presupuesto.query.get(id)

    if request.method == 'POST':
        # Aquí manejas la actualización del contacto según los datos del formulario
        marca_actualizado = request.form['marca']
        segmento_actualizado = request.form['segmento']
        reparacion_actualizado = request.form['reparacion']
        precio_actualizado = request.form['precio']
        fechaActualizacion_actualizado = request.form['fechaActualizacion']
        observacion_actualizado = request.form['observacion']
        
    return render_template('seleccionar_presupuesto.html', presupuesto=presupuesto)

@app.route('/borrar_presupuesto/<int:id>')
def borrar_presupuesto(id):
    presupuesto = Presupuesto.query.get(id)

    if presupuesto:
        db.session.delete(presupuesto)
        db.session.commit()
        return ('exito borrar')
    else:
        return ('no existe contacto')
    
    
@app.route('/buscar_presupuesto', methods=['GET', 'POST'])
def buscar_presupuesto():
    marca = request.args.get('marca')
    segmento = request.args.get('segmento')
    reparacion = request.args.get('reparacion')
    presupuestos = Presupuesto.query.all()
    marcas = db.session.query(Presupuesto.marca).distinct().all()
    segmentos = db.session.query(Presupuesto.segmento).distinct().all()
    reparaciones = db.session.query(Presupuesto.reparacion).distinct().all()

    print("Valores recibidos:", marca, segmento, reparacion)  # Verificar valores recibidos

    # Inicializa una lista para almacenar los resultados de la búsqueda
    resultados = []

    # Realizamos la búsqueda en la base de datos solo si se proporciona al menos un parámetro de búsqueda
    if marca or segmento or reparacion:
        # Construimos la consulta filtrando por los parámetros proporcionados
        consulta = Presupuesto.query

        # Filtrar por marca si no es "Todas las marcas"
        if marca and marca.lower() != 'todas las marcas':
            consulta = consulta.filter(Presupuesto.marca.ilike(f"%{marca}%"))

        # Filtrar por segmento si no es "Todos los segmentos"
        if segmento and segmento.lower() != 'todos los segmentos':
            consulta = consulta.filter(Presupuesto.segmento.ilike(f"%{segmento}%"))

        # Filtrar por reparacion si no es "Todas las reparaciones"
        if reparacion and reparacion.lower() != 'todas las reparaciones':
            consulta = consulta.filter(Presupuesto.reparacion.ilike(f"%{reparacion}%"))

        # Ejecutamos la consulta y almacenamos los resultados en la lista
        resultados = consulta.all()

    print("Resultados de la búsqueda:", resultados)  # Verificar resultados de la búsqueda

    return render_template('buscar_presupuesto.html', presupuestos=presupuestos, marcas=marcas, segmentos=segmentos, reparaciones=reparaciones, resultados=resultados, marca=marca, segmento=segmento, reparacion=reparacion)
    
    

    
# def __init__(self, marca, segmento, reparacion, precio, fechaActualizacion, observacion):
#         self.marca = marca
#         self.segmento = segmento
#         self.reparacion = reparacion
#         self.precio = precio
#         self.fechaActualizacion = fechaActualizacion
#         self.observacion = observacion

# # Lista de ejemplos de presupuestos
# presupuestos = [
#     Presupuesto("Renault", "Segmento1", "Reparacion1", 1000.0, "2024-01-01", "Observacion1"),
#     Presupuesto("Renault", "Segmento2", "Reparacion2", 1200.0, "2024-01-02", "Observacion2"),
#     # Agrega más ejemplos según sea necesario
# ]

@app.route('/opciones_segmento_reparacion/<marca>')
def opciones_segmento_reparacion(marca):
    segmentos = db.session.query(Presupuesto.segmento).filter_by(marca=marca).distinct().all()
    reparaciones = db.session.query(Presupuesto.reparacion).filter_by(marca=marca).distinct().all()

    opciones = {
        "segmentos": [segmento[0] for segmento in segmentos],
        "reparaciones": [reparacion[0] for reparacion in reparaciones]
    }
    return jsonify(opciones)






    
    
    
    
    
    
    
@app.route('/buscar_marca')
def buscar_marca():
    presupuestos = Presupuesto.query.all()
    comentarios = Comentario.query.all()
    return render_template('buscar_marca.html', presupuestos=presupuestos, comentarios=comentarios)   
    
    
@app.route('/renault')
def renault():
    presupuestos = Presupuesto.query.all()
    return render_template('renault.html', presupuestos=presupuestos)

@app.route('/volkswagen')
def volkswagen():
    presupuestos = Presupuesto.query.all()
    return render_template('volkswagen.html', presupuestos=presupuestos)

@app.route('/chevrolet')
def chevrolet():
    presupuestos = Presupuesto.query.all()
    return render_template('chevrolet.html', presupuestos=presupuestos)

@app.route('/fiat')
def fiat():
    presupuestos = Presupuesto.query.all()
    return render_template('fiat.html', presupuestos=presupuestos)

@app.route('/ford')
def ford():
    presupuestos = Presupuesto.query.all()
    return render_template('ford.html', presupuestos=presupuestos)

@app.route('/toyota')
def toyota():
    presupuestos = Presupuesto.query.all()
    return render_template('toyota.html', presupuestos=presupuestos)

@app.route('/audi')
def audi():
    presupuestos = Presupuesto.query.all()
    return render_template('audi.html', presupuestos=presupuestos)

@app.route('/bmw')
def bmw():
    presupuestos = Presupuesto.query.all()
    return render_template('bmw.html', presupuestos=presupuestos)

@app.route('/peugeot')
def peugeot():
    presupuestos = Presupuesto.query.all()
    return render_template('peugeot.html', presupuestos=presupuestos)

@app.route('/mercedes')
def mercedes():
    presupuestos = Presupuesto.query.all()
    return render_template('mercedes.html', presupuestos=presupuestos)






# Lista para almacenar los comentarios
comentarios = []

@app.route('/ver_comentarios', methods=['GET'])
def ver_comentarios():
    comentarios = Comentario.query.order_by(Comentario.fecha.desc()).all()
    return render_template('ver_comentarios.html', comentarios=comentarios)

# Ruta para mostrar el formulario
@app.route('/agregar_comentario', methods=['GET'])
def mostrar_formulario():
    return render_template('comentario.html')

# Ruta para procesar el formulario
@app.route('/agregar_comentario', methods=['POST'])
def agregar_comentario():
    nombre = request.form.get('nombre')
    vehiculo = request.form.get('vehiculo')
    mensaje = request.form.get('mensaje')

    nuevo_comentario = Comentario(nombre=nombre, vehiculo=vehiculo, mensaje=mensaje)

    db.session.add(nuevo_comentario)
    db.session.commit()

    return redirect(url_for('ver_comentarios'))















if __name__ == "__main__":
    # Crear las tablas antes de ejecutar
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)