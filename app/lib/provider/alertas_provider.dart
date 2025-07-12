import 'package:kk/modelos/modelo_alerta.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AlertasProvider extends ChangeNotifier {
  bool isLoading = false;
  List<Alerta> alertas = [];
  // Variable para saber si los datos estan cargando o no

  Future<void> FetchAlertas() async {
    isLoading = true;
    notifyListeners(); // Escuchas movimientos realizados

    final url =
    Uri.parse('http://192.168.0.33:5000/alerts'); // Variable url para API

    try {
      final response = await http.get(
          url); // Esperar respuesta de URL y Se guarda en response lo que obtiene
      if (response.statusCode == 200) {
        final data = jsonDecode(
            response.body); // Castear lo el cuerpo recibido a formato JSON
        alertas = List<Alerta>.from(
            data['alertas'].map((alerta) => Alerta.fromJSON(alerta)));
      } else {
        print(Text('Error ${response.statusCode}'));
        alertas = [];
      }
    } catch (e) {
      print('Error en la solicitud');
      alertas = [];
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}
