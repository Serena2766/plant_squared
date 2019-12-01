import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:convert';

/*
Project Group T5
Plant Squared
Main developer: Jerry Xiong

App for Monitoring and Controlling a plant
 */


//main function runs the app and awaits a UPD message
void main() {

  runApp(MyApp());

  //var address = new InternetAddress('172.16.32.73');
  var address = new InternetAddress('127.0.0.1');
  RawDatagramSocket.bind(address, 9003).then((udpSocket) {

    //Waiting to receive data packet containing plant info

    udpSocket.listen((e) {
      print(e.toString());
      Datagram dg = udpSocket.receive();
      if(dg != null)
        dg.data.forEach((x) => print(x));
      //check if the "toString()" function works
      //if(dg.data.contains(''))

    });
  });
}

//Send UPD packets based on
void _sendCommand(var x) {
  print('send command function: '  + '$x');

  //var data = "Hello, World";
  var codec = new Utf8Codec();
  //List<int> dataToSend = codec.encode(data);
  List<int> dataToSend = codec.encode(x);
  print(dataToSend);

  //var address = new InternetAddress('172.16.32.73');
  var address = new InternetAddress('127.0.0.1');
  RawDatagramSocket.bind(address, 9003).then((udpSocket) {

    udpSocket.send(dataToSend, new InternetAddress('172.16.32.73'), 9003);
    print('Did send data on the stream..');
  });
}

//Sends a UDP message requestions picture data
//Receive picture data
void _videoReceiver()
{
  

}


class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);


  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Invoke "debug painting" (press "p" in the console, choose the
          // "Toggle Debug Paint" action from the Flutter Inspector in Android
          // Studio, or the "Toggle Debug Paint" command in Visual Studio Code)
          // to see the wireframe for each widget.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.display1,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
