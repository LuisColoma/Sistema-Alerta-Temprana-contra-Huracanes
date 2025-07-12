import numpy as np
import os

from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector
from tflite_support import metadata
import tensorflow as tf

assert tf.__version__.startswith('2')
tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)



train_data = object_detector.DataLoader.from_pascal_voc(
    '/home/luis/proyect_p39/deteccion/Imagenes satelitales/entrenamiento',
    '/home/luis/proyect_p39/deteccion/Imagenes satelitales/entrenamiento',
    ['precipitacion']
)

validate_data = object_detector.DataLoader.from_pascal_voc(
    '/home/luis/proyect_p39/deteccion/Imagenes satelitales/Validate',
    '/home/luis/proyect_p39/deteccion/Imagenes satelitales/Validate',
    ['precipitacion']
)

spec = model_spec.get('efficientdet_lite0')

model = object_detector.create(train_data, model_spec = spec, batch_size=4, train_whole_model=True, epochs=20, validation_data=validate_data)

model.evaluate(validate_data)

model.export(export_dir='.', tflite_filename='huracan.tflite')

print("Validacion del modelo: ")

model.evaluate_tflite('huracan.tflite', validate_data)
