import 'package:kk/screens/Detalle_alerta.dart';
import 'package:kk/screens/RealidaAumentada.dart';
import 'package:kk/provider/alertas_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class MainHome extends StatelessWidget {
  const MainHome({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final alertasProvider =
    Provider.of<AlertasProvider>(context, listen: false);
    alertasProvider.FetchAlertas();
    return Scaffold(
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            Container(
              height: 95,
              child: DrawerHeader(
                decoration: BoxDecoration(
                  color: const Color.fromARGB(255, 17, 119, 202),
                ),
                child: Text(
                  'Menú Principal',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                  ),
                ),
              ),
            ),
            ListTile(
              leading: Icon(Icons.view_in_ar),
              title: Text('Realidad Aumentada'),
              onTap: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => WithARkitScreen()));
              },
            ),
            ListTile(
              leading: Icon(Icons.help_outline),
              title: Text('Preguntas Frecuentes'),
            )
          ],
        ),
      ),
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 17, 119, 202),
        title: Title(
            color: Colors.white,
            child: Text('Alerta de Huracán',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 27,
                ))),
        iconTheme: IconThemeData(
          color: Colors.white,
        ),
      ),
      body: Consumer<AlertasProvider>(builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        } else if (provider.alertas.isEmpty) {
          return const Center(
            child: Text('sin datos de alertas'),
          );
        } else {
          return ListView(padding: EdgeInsets.all(5), children: <Widget>[
            _ImagSatelital(context, provider),
            ListView.builder(
                shrinkWrap:
                true, // Importante para que funcione dentro de otro ListView
                physics: NeverScrollableScrollPhysics(), // Evita doble scroll
                itemCount: provider.alertas.length,
                itemBuilder: (context, index) {
                  return _AlertaCard(context, provider.alertas[index]);
                }),
          ]);
        }
      }),
    );
  }
}

Widget _ImagSatelital(BuildContext context, AlertasProvider provider) {
  final alertaReciente = provider.alertas.last;
  return Padding(
    padding: const EdgeInsets.all(8.0),
    child: Container(
      width: MediaQuery.of(context).size.width,
      height: 500,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          SizedBox(
            width: 5,
          ),
          Container(
            child: Text(
              'Detalles de última Alerta',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          Container(
            //color: const Color.fromARGB(248, 250, 250, 250),
            child: Column(
              children: [
                SizedBox(
                  height: 12.5,
                ),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    SizedBox(
                      width: 10,
                    ),
                    Text(
                      'Fecha de análisis:',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(
                      width: 105,
                    ),
                    Text(
                      'Precipitaciones:',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                    )
                  ],
                ),
                Row(
                  children: [
                    SizedBox(
                      width: 25,
                    ),
                    Text('${alertaReciente.received_at}'),
                    SizedBox(
                      width: 230,
                    ),
                    Text('${alertaReciente.detecciones}')
                  ],
                ),
                SizedBox(
                  height: 5,
                )
              ],
            ),
          ),
          Container(
            height: 360,
            width: MediaQuery.of(context).size.width,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(13),
              child: Image.network(
                'http://192.168.0.33:5000${alertaReciente.image_url}',
                fit: BoxFit.cover,
              ),
            ),
            //decoration: BoxDecoration(
            //borderRadius: BorderRadius.circular(10), color: Colors.amber),
          ),
          SizedBox(
            height: 22,
          ),
          Text(
            'Historial de Alertas',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
      //child: Text('Imagen Satelital'),
    ),
  );
}

// Widget con información real con detalle de alertas
Widget _AlertaCard(BuildContext context, dynamic alerta) {
  return GestureDetector(
    onTap: () {
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => DetalleAlerta(IDAlerta: alerta.id)));
    },
    child: SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(1.0),
        child: Container(
          width: MediaQuery.of(context).size.width,
          height: 110,
          child: Card(
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: Colors.black26)),
            child: Row(
              children: <Widget>[
                SizedBox(
                  width: 26,
                ),
                Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    //Padding(padding: const EdgeInsets.all(7.0)),
                    Text('ID: ${alerta.id}'),
                    SizedBox(
                      height: 2,
                    ),
                    Text('Fecha: ${alerta.received_at}'),
                    SizedBox(
                      height: 2,
                    ),
                    Text('No. de precipitaciones: ${alerta.detecciones}'),
                  ],
                )
              ],
            ),
          ),
        ),
      ),
    ),
  );
}
