class Alerta {
  String id;
  String received_at;
  String detecciones;
  String image_url;

  Alerta({
    required this.id,
    required this.received_at,
    required this.detecciones,
    required this.image_url,
  });

  factory Alerta.fromJSON(Map<String, dynamic> json) {
    return Alerta(
        id: json['id'],
        received_at: json['received_at'],
        detecciones: json['detecciones'],
        image_url: json['image_url']);
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'received_at': received_at,
      'detecciones': detecciones,
      'image_url': image_url
    };
  }

  @override
  String toString() {
    return 'Alerta{id: $id, received_at: $received_at, detecciones: $detecciones, image_url: $image_url}';
  }
}