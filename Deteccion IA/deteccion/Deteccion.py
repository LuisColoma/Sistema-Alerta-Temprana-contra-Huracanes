import argparse
import datetime
import sys
import time
import cv2
import requests
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
import numpy as np
from tflite_support.task import processor
from twilio.rest import Client
from datetime import datetime

fecha_utc = datetime.utcnow().isoformat() + "Z"
fecha_formateada1 = fecha_utc[:10]
fecha_formateada = "2024-09-14"
# Tu SID y Token de la consola de Twilio
account_sid = ' '
auth_token = ' '
client = Client(account_sid, auth_token)

# URL del servidor de API
API_URL = "http://192.168.0.33:5000/alerts"

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red


GUATEMALA_REGION = {
    "x_min": 131,
    "x_max": 380,
    "y_min": 154,
    "y_max": 418
}

def envio_server_API(lat, lon, detecciones):
  payload = {
    "lat": lat,
    "lon": lon,
    "detecciones": detecciones,
  }
  try:
      r = requests.post(API_URL, json=payload, timeout=5)
      if r.status_code == 201:
          print("✅ Alerta enviada al servidor")
      else:
          print("Error al enviar alerta:", r.status_code)
  except Exception as e:
      print("Excepción enviando alerta:", e)

def run(model: str, image_path: str, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:
  """Run inference on a single image from a file."""

  # Variables para calcular FPS (opcional aquí, para medir el tiempo de ejecución)
  counter, fps = 0, 0
  start_time = time.time()

  # Cargar la imagen desde el archivo en lugar de capturarla desde la cámara
  image = cv2.imread('/home/luis/proyect_p39/deteccion/Imagenes satelitales/Validate/img_{0}.jpg'.format(fecha_formateada))
  if image is None:
    sys.exit(f"ERROR: Unable to read the image from {image_path}")

  # Cambiar el tamaño de la imagen para que coincida con el tamaño de entrada del modelo
  image_resized = cv2.resize(image, (width, height))

  # Parámetros de visualización
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # Inicializar el modelo de detección de objetos
  base_options = core.BaseOptions(
      file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
  detection_options = processor.DetectionOptions(
      max_results=3, score_threshold=0.3)
  options = vision.ObjectDetectorOptions(
      base_options=base_options, detection_options=detection_options)
  detector = vision.ObjectDetector.create_from_options(options)

  # Convierte la imagen de BGR a RGB según lo requiera el modelo TFLite.
  rgb_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

  # Crea un objeto TensorImage a partir de la imagen RGB.
  input_tensor = vision.TensorImage.create_from_array(rgb_image)

  # Ejecute la estimación de detección de objetos utilizando el modelo.
  detection_result = detector.detect(input_tensor)

  # Visualizar los resultados de la detección en la imagen
  image = utils.visualize(image_resized, detection_result)

  # Obtener parametros de cajita
  parametros = utils.parametros(image_resized, detection_result)
  #print('Las cordenadas son: ', parametros, ' sus caracteristicas: ', type(parametros), ' y sus dimensiones: ', len(parametros))
  datos_x = parametros[0]
  datos_y = parametros[1]
  detecciones = parametros[2]
  print('Las cordenadas X son: ', datos_x, ' sus caracteristicas: ', type(datos_x))
  print('Las cordenadas Y son: ', datos_y, ' sus caracteristicas: ', type(datos_x))
  print('Cantidad de detecciones',detecciones)

  for i in range(detecciones):
    if GUATEMALA_REGION["x_min"] < datos_x[i] < GUATEMALA_REGION["x_max"]:
      print('Coordenada en X: ',datos_x[i])
      #print('Esta dentro de X')
      if GUATEMALA_REGION["y_min"] < datos_y[i] < GUATEMALA_REGION["y_max"]:
        print('Coordenada en Y: ',datos_y[i])
        #print('Esta dentro de Y')
        #print('HURACAN EN GUATEMALA')
        message = client.messages.create(
          body='Alerta de huracán detectada en tu zona. Toma precauciones.',
          from_='+18382311617',  # Número de Twilio
          to='+50251612538'       # Número destino (Guatemala u otro)
          )
        print(f'Mensaje enviado: {message.sid}')
        time.sleep(2)
        cantidad_detecc = str(detecciones)
        envio_server_API(5,3,cantidad_detecc)
        


  # Mostrar FPS (aunque en realidad no se usa para imágenes estáticas)
  end_time = time.time()
  fps = 1 / (end_time - start_time)
  fps_text = 'FPS = {:.1f}'.format(fps)
  text_location = (left_margin, row_size)
  cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
              font_size, text_color, font_thickness)

  # Mostrar el resultado
  cv2.imshow('object_detector', image)
  cv2.waitKey(0)  # Esperar hasta que se presione una tecla
  cv2.destroyAllWindows()






def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--imagePath', help='Path to the image file.', required=True)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  args = parser.parse_args()

  run(args.model, args.imagePath, args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
  main()
