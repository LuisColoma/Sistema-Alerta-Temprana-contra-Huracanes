import 'package:flutter/material.dart';

class DetalleAlerta extends StatelessWidget {
  final String IDAlerta;
  const DetalleAlerta({Key? key, required this.IDAlerta}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          IDAlerta,
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: const Color.fromARGB(255, 17, 119, 202),
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Icon(Icons.arrow_back),
          color: Colors.white,
        ),
      ),
    );
  }
}
