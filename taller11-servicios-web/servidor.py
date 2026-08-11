import json
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import List


@dataclass
class Pregunta:
    """Representa un ejercicio con su enunciado, sus 3 opciones y la solución correcta (A, B o C)."""
    pregunta: str
    opcion_a: str
    opcion_b: str
    opcion_c: str
    solucion: str


# Aquí se parametriza el arreglo de preguntas.
PREGUNTAS: List[Pregunta] = [
    Pregunta(
        pregunta="for i &blank 0; i &lt; 10; i++",
        opcion_a="=",
        opcion_b="<",
        opcion_c=":=",
        solucion="C",
    ),
    Pregunta(
        pregunta='var nombre &blank "Sofia"',
        opcion_a="=",
        opcion_b="<",
        opcion_c=":=",
        solucion="A",
    ),
]


class Pagina:
    """Encapsula la plantilla HTML e inyecta el arreglo de preguntas como JSON."""

    _PLACEHOLDER = "__PREGUNTAS_JSON__"

    _TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Completa el for</title>
<style>
  body {
    font-family: -apple-system, Arial, sans-serif;
    background: #f2f2f2;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
  }
  .card {
    background: #fff;
    padding: 32px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    width: 480px;
    box-sizing: border-box;
  }

  /* ---------- Pantalla inicio ---------- */
  #pantalla-inicio {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
  }
  #pantalla-inicio h2 {
    margin: 0;
    color: #333;
  }
  #inputNombre {
    width: 100%;
    box-sizing: border-box;
    font-size: 20px;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ccc;
    text-align: center;
  }
  #btnIniciar {
    width: 100%;
    font-size: 22px;
    padding: 14px;
    border: none;
    border-radius: 8px;
    background: #007acc;
    color: #fff;
    cursor: pointer;
  }
  #btnIniciar:hover {
    background: #005f99;
  }

  /* ---------- Pantalla pregunta ---------- */
  #pantalla-pregunta {
    display: none;
    flex-direction: column;
    align-items: center;
  }
  .code {
    width: 100%;
    box-sizing: border-box;
    height: 160px;
    font-family: 'Courier New', monospace;
    font-size: 24px;
    background: #1e1e1e;
    color: #d4d4d4;
    border-radius: 8px;
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .blank {
    font-weight: bold;
    color: #ffcc00;
  }
  .blank.correcto {
    color: #4caf50;
  }
  .blank.incorrecto {
    color: #e74c3c;
  }
  .variable {
    width: 100%;
    font-size: 26px;
    color: #555;
    margin-bottom: 20px;
    min-height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .buttons {
    display: flex;
    justify-content: center;
    gap: 14px;
  }
  .buttons button {
    width: 143px;
    height: 143px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Courier New', monospace;
    font-size: 42px;
    padding: 0;
    border: none;
    border-radius: 8px;
    background: #007acc;
    color: #fff;
    cursor: pointer;
  }
  .buttons button:hover {
    background: #005f99;
  }

  /* ---------- Pantalla final ---------- */
  #pantalla-final {
    display: none;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 14px;
  }
  #pantalla-final h2 {
    margin: 0;
    color: #333;
  }
  #listaFinal {
    width: 100%;
    box-sizing: border-box;
    text-align: left;
    background: #f7f7f7;
    border-radius: 8px;
    padding: 16px 16px 16px 36px;
    margin: 0;
  }
  #listaFinal li {
    font-family: 'Courier New', monospace;
    margin-bottom: 8px;
    color: #333;
  }
</style>
</head>
<body>
  <div class="card">

    <!-- Pantalla 1: pedir nombre -->
    <div id="pantalla-inicio">
      <h2>¿Cuál es tu nombre?</h2>
      <input id="inputNombre" type="text" placeholder="Escribe tu nombre">
      <button id="btnIniciar" onclick="iniciar()">Iniciar</button>
    </div>

    <!-- Pantalla 2: pregunta -->
    <div id="pantalla-pregunta">
      <div class="code" id="code"></div>
      <div class="variable" id="variable">Elige un operador</div>
      <div class="buttons">
        <button id="btnA"></button>
        <button id="btnB"></button>
        <button id="btnC"></button>
      </div>
    </div>

    <!-- Pantalla 3: final -->
    <div id="pantalla-final">
      <h2 id="tituloFinal"></h2>
      <ul id="listaFinal"></ul>
    </div>

  </div>

  <script>
    const preguntas = __PREGUNTAS_JSON__;
    let nombre = '';
    let indice = 0;
    const respondidas = [];

    function iniciar() {
      const valor = document.getElementById('inputNombre').value.trim();
      if (!valor) {
        document.getElementById('inputNombre').focus();
        return;
      }
      nombre = valor;
      document.getElementById('pantalla-inicio').style.display = 'none';
      document.getElementById('pantalla-pregunta').style.display = 'flex';
      cargarPregunta(indice);
    }

    function cargarPregunta(i) {
      const p = preguntas[i];

      const html = p.pregunta.replace(
        '&blank',
        '<span id="blank" class="blank">___</span>'
      );
      document.getElementById('code').innerHTML = html;
      document.getElementById('variable').textContent = 'Elige un operador';

      const btnA = document.getElementById('btnA');
      const btnB = document.getElementById('btnB');
      const btnC = document.getElementById('btnC');

      btnA.textContent = p.opcion_a;
      btnB.textContent = p.opcion_b;
      btnC.textContent = p.opcion_c;

      btnA.onclick = () => elegir(p.opcion_a, 'A');
      btnB.onclick = () => elegir(p.opcion_b, 'B');
      btnC.onclick = () => elegir(p.opcion_c, 'C');
    }

    function elegir(valor, letra) {
      const p = preguntas[indice];
      const blank = document.getElementById('blank');
      blank.textContent = valor;

      if (letra === p.solucion) {
        blank.classList.remove('incorrecto');
        blank.classList.add('correcto');
        document.getElementById('variable').textContent = '¡Correcto!';

        const textoCompleto = p.pregunta
          .replace('&blank', valor)
          .replace(/&lt;/g, '<');
        respondidas.push(textoCompleto);

        setTimeout(() => {
          indice++;
          if (indice < preguntas.length) {
            cargarPregunta(indice);
          } else {
            mostrarFinal();
          }
        }, 700);
      } else {
        blank.classList.remove('correcto');
        blank.classList.add('incorrecto');
        document.getElementById('variable').textContent = 'Incorrecto, intenta de nuevo';
      }
    }

    function mostrarFinal() {
      document.getElementById('pantalla-pregunta').style.display = 'none';
      document.getElementById('pantalla-final').style.display = 'flex';
      document.getElementById('tituloFinal').textContent =
        '¡Felicidades, ' + nombre + '!';

      const lista = document.getElementById('listaFinal');
      lista.innerHTML = '';
      respondidas.forEach(texto => {
        const li = document.createElement('li');
        li.textContent = texto;
        lista.appendChild(li);
      });
    }
  </script>
</body>
</html>"""

    def __init__(self, preguntas: List[Pregunta]):
        self.preguntas = preguntas

    def render(self) -> bytes:
        """Sustituye el placeholder por el JSON de las preguntas y devuelve el HTML en bytes."""
        preguntas_json = json.dumps(
            [asdict(p) for p in self.preguntas], ensure_ascii=False
        )
        html = self._TEMPLATE.replace(self._PLACEHOLDER, preguntas_json)
        return html.encode("utf-8")


class ForHandler(BaseHTTPRequestHandler):
    """Maneja las peticiones HTTP entrantes."""

    pagina = Pagina(PREGUNTAS)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "No encontrado")
            return

        contenido = self.pagina.render()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def log_message(self, format, *args):
        print("%s - %s" % (self.client_address[0], format % args))


class Servidor:
    """Encapsula la creación y ejecución del servidor HTTP."""

    def __init__(self, host: str = "localhost", puerto: int = 8080):
        self.host = host
        self.puerto = puerto
        self._httpd = ThreadingHTTPServer((self.host, self.puerto), ForHandler)

    def iniciar(self):
        print(f"Servidor corriendo en http://{self.host}:{self.puerto}")
        try:
            self._httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
        finally:
            self._httpd.server_close()


if __name__ == "__main__":
    Servidor(host="localhost", puerto=8080).iniciar()
