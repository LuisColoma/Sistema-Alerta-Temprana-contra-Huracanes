import 'package:kk/screens/mainHome.dart';
import 'package:kk/provider/alertas_provider.dart';
import 'package:flutter/material.dart';
// ignore: unused_import
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
//import 'package:flutter_unity_widget/flutter_unity_widget.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [ChangeNotifierProvider(create: (_) => AlertasProvider())],
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Flutter Demo',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: const MainHome(),
      ),
    );
  }
}

class Barra extends StatelessWidget {
  const Barra({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 1,
      child: Scaffold(
        //drawer: Drawer(),
          appBar: AppBar(
            title: Text('Alerta de Huracanes'),
            titleTextStyle: TextStyle(color: Colors.white, fontSize: 20),
            backgroundColor: Colors.blue,
            bottom: TabBar(
                indicatorColor: Colors.white,
                labelColor: Colors.white,
                unselectedLabelColor: Colors.white,
                tabs: [
                  Tab(
                    icon: Icon(Icons.home),
                    text: 'Casa',
                  ),
                  //Tab(
                  //icon: Icon(Icons.settings),
                  //text: 'Opciones',
                  //)
                ]),
          ),
          body: TabBarView(children: [MainHome()])),
    );
  }
}
