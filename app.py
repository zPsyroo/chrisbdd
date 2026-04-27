from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="192.168.1.153",
        user="flask_user",
        password="flask1234",
        database="veterinaria"
    )

# ── INICIO ──
@app.route("/")
def index():
    return redirect(url_for("animales"))

# ── ANIMALES ──
@app.route("/animales")
def animales():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT animales.*, duenos.nombre AS dueno_nombre
        FROM animales
        LEFT JOIN duenos ON animales.dueno_id = duenos.id
    """)
    lista = cur.fetchall()
    db.close()
    return render_template("animales.html", animales=lista)

@app.route("/animales/nuevo", methods=["GET", "POST"])
def nuevo_animal():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM duenos")
    duenos = cur.fetchall()
    if request.method == "POST":
        cur.execute("""
            INSERT INTO animales (nombre, especie, raza, edad, dueno_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (request.form["nombre"], request.form["especie"], request.form["raza"], request.form["edad"], request.form["dueno_id"] or None))
        db.commit()
        db.close()
        return redirect(url_for("animales"))
    db.close()
    return render_template("form_animal.html", animal=None, duenos=duenos)

@app.route("/animales/editar/<int:id>", methods=["GET", "POST"])
def editar_animal(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM duenos")
    duenos = cur.fetchall()
    if request.method == "POST":
        cur.execute("""
            UPDATE animales SET nombre=%s, especie=%s, raza=%s, edad=%s, dueno_id=%s WHERE id=%s
        """, (request.form["nombre"], request.form["especie"], request.form["raza"], request.form["edad"], request.form["dueno_id"] or None, id))
        db.commit()
        db.close()
        return redirect(url_for("animales"))
    cur.execute("SELECT * FROM animales WHERE id=%s", (id,))
    animal = cur.fetchone()
    db.close()
    return render_template("form_animal.html", animal=animal, duenos=duenos)

@app.route("/animales/borrar/<int:id>")
def borrar_animal(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM animales WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("animales"))

# ── DUEÑOS ──
@app.route("/duenos")
def duenos():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM duenos")
    lista = cur.fetchall()
    db.close()
    return render_template("duenos.html", duenos=lista)

@app.route("/duenos/nuevo", methods=["GET", "POST"])
def nuevo_dueno():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO duenos (nombre, telefono, email) VALUES (%s, %s, %s)",
            (request.form["nombre"], request.form["telefono"], request.form["email"]))
        db.commit()
        db.close()
        return redirect(url_for("duenos"))
    return render_template("form_dueno.html", dueno=None)

@app.route("/duenos/editar/<int:id>", methods=["GET", "POST"])
def editar_dueno(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    if request.method == "POST":
        cur.execute("UPDATE duenos SET nombre=%s, telefono=%s, email=%s WHERE id=%s",
            (request.form["nombre"], request.form["telefono"], request.form["email"], id))
        db.commit()
        db.close()
        return redirect(url_for("duenos"))
    cur.execute("SELECT * FROM duenos WHERE id=%s", (id,))
    dueno = cur.fetchone()
    db.close()
    return render_template("form_dueno.html", dueno=dueno)

@app.route("/duenos/borrar/<int:id>")
def borrar_dueno(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM duenos WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("duenos"))

# ── VETERINARIOS ──
@app.route("/veterinarios")
def veterinarios():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM veterinarios")
    lista = cur.fetchall()
    db.close()
    return render_template("veterinarios.html", veterinarios=lista)

@app.route("/veterinarios/nuevo", methods=["GET", "POST"])
def nuevo_veterinario():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO veterinarios (nombre, especialidad, telefono) VALUES (%s, %s, %s)",
            (request.form["nombre"], request.form["especialidad"], request.form["telefono"]))
        db.commit()
        db.close()
        return redirect(url_for("veterinarios"))
    return render_template("form_veterinario.html", veterinario=None)

@app.route("/veterinarios/editar/<int:id>", methods=["GET", "POST"])
def editar_veterinario(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    if request.method == "POST":
        cur.execute("UPDATE veterinarios SET nombre=%s, especialidad=%s, telefono=%s WHERE id=%s",
            (request.form["nombre"], request.form["especialidad"], request.form["telefono"], id))
        db.commit()
        db.close()
        return redirect(url_for("veterinarios"))
    cur.execute("SELECT * FROM veterinarios WHERE id=%s", (id,))
    veterinario = cur.fetchone()
    db.close()
    return render_template("form_veterinario.html", veterinario=veterinario)

@app.route("/veterinarios/borrar/<int:id>")
def borrar_veterinario(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM veterinarios WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("veterinarios"))

# ── CITAS ──
@app.route("/citas")
def citas():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT citas.*, animales.nombre AS animal_nombre, veterinarios.nombre AS veterinario_nombre
        FROM citas
        LEFT JOIN animales ON citas.animal_id = animales.id
        LEFT JOIN veterinarios ON citas.veterinario_id = veterinarios.id
    """)
    lista = cur.fetchall()
    db.close()
    return render_template("citas.html", citas=lista)

@app.route("/citas/nuevo", methods=["GET", "POST"])
def nueva_cita():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM animales")
    animales = cur.fetchall()
    cur.execute("SELECT * FROM veterinarios")
    veterinarios = cur.fetchall()
    if request.method == "POST":
        cur.execute("INSERT INTO citas (fecha, motivo, animal_id, veterinario_id) VALUES (%s, %s, %s, %s)",
            (request.form["fecha"], request.form["motivo"], request.form["animal_id"], request.form["veterinario_id"]))
        db.commit()
        db.close()
        return redirect(url_for("citas"))
    db.close()
    return render_template("form_cita.html", cita=None, animales=animales, veterinarios=veterinarios)

@app.route("/citas/editar/<int:id>", methods=["GET", "POST"])
def editar_cita(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM animales")
    animales = cur.fetchall()
    cur.execute("SELECT * FROM veterinarios")
    veterinarios = cur.fetchall()
    if request.method == "POST":
        cur.execute("UPDATE citas SET fecha=%s, motivo=%s, animal_id=%s, veterinario_id=%s WHERE id=%s",
            (request.form["fecha"], request.form["motivo"], request.form["animal_id"], request.form["veterinario_id"], id))
        db.commit()
        db.close()
        return redirect(url_for("citas"))
    cur.execute("SELECT * FROM citas WHERE id=%s", (id,))
    cita = cur.fetchone()
    db.close()
    return render_template("form_cita.html", cita=cita, animales=animales, veterinarios=veterinarios)

@app.route("/citas/borrar/<int:id>")
def borrar_cita(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM citas WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("citas"))

# ── TRATAMIENTOS ──
@app.route("/tratamientos")
def tratamientos():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT tratamientos.*, citas.motivo AS cita_motivo
        FROM tratamientos
        LEFT JOIN citas ON tratamientos.cita_id = citas.id
    """)
    lista = cur.fetchall()
    db.close()
    return render_template("tratamientos.html", tratamientos=lista)

@app.route("/tratamientos/nuevo", methods=["GET", "POST"])
def nuevo_tratamiento():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM citas")
    citas = cur.fetchall()
    if request.method == "POST":
        cur.execute("INSERT INTO tratamientos (descripcion, medicamento, dosis, cita_id) VALUES (%s, %s, %s, %s)",
            (request.form["descripcion"], request.form["medicamento"], request.form["dosis"], request.form["cita_id"]))
        db.commit()
        db.close()
        return redirect(url_for("tratamientos"))
    db.close()
    return render_template("form_tratamiento.html", tratamiento=None, citas=citas)

@app.route("/tratamientos/editar/<int:id>", methods=["GET", "POST"])
def editar_tratamiento(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM citas")
    citas = cur.fetchall()
    if request.method == "POST":
        cur.execute("UPDATE tratamientos SET descripcion=%s, medicamento=%s, dosis=%s, cita_id=%s WHERE id=%s",
            (request.form["descripcion"], request.form["medicamento"], request.form["dosis"], request.form["cita_id"], id))
        db.commit()
        db.close()
        return redirect(url_for("tratamientos"))
    cur.execute("SELECT * FROM tratamientos WHERE id=%s", (id,))
    tratamiento = cur.fetchone()
    db.close()
    return render_template("form_tratamiento.html", tratamiento=tratamiento, citas=citas)

@app.route("/tratamientos/borrar/<int:id>")
def borrar_tratamiento(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tratamientos WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("tratamientos"))

if __name__ == "__main__":
    app.run(debug=True)
