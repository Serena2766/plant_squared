import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:convert';

/*
Project Group T5
Plant Squared
Main developer: Jerry Xiong

App for Monitoring and Controlling a plant
 */


//main function runs the app
void main() {
  runApp(MyApp());

}

//Send UPD packets based on user command is given
void _sendCommand(var x) {
  print('send command function: '  + '$x');

  //var data = "Hello, World";
  var codec = new Utf8Codec();
  //List<int> dataToSend = codec.encode(data);
  List<int> dataToSend = codec.encode(x);
  print('$dataToSend');

  //var address = new InternetAddress('172.16.32.73');
  var address = new InternetAddress('127.0.0.1');
  RawDatagramSocket.bind(address, 9003).then((udpSocket) {

    udpSocket.send(dataToSend, new InternetAddress('172.16.32.73'), 9003);
    print('Did send data on the stream..');
  });
}


void _todo()
{


}


class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.green, //affects icon button

        primaryColor: Colors.teal, //affects app bar
        brightness: Brightness.light,
      ),
      home: MyHomePage(title: 'Plant Squared'),
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

  //Function for setting up the connection for receiving data
  void setUpSocket()
  {
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

  //****************************************
  //              Variables
  //****************************************
  //The type of plant
  int _plantType = 5; // start as N/A

  //The current conditions
  double _waterLevel = 0;
  double _temperature = 0;
  double _humidity = 0;

  //The ideal conditions
  double _idealWaterLevel = 0;
  double _idealTemperature = 0;
  double _idealHumidity = 0;

  //Central image and name of plant
  Image _mainImage;
  String _plantName;

  @override
  initState(){
    _mainImage = Image.asset('assets/flower.png');
    _plantName = 'Default Flower';
    setUpSocket(); //jx Not sure if here
  }
  //****************************************

  //Sends a UDP message requests picture data
  //Receive picture data
  void _videoReceiver()
  {
    print('videoReceiver Function');
    //for now let's change the main image
    setState(() {
      _mainImage = new Image.asset('assets/flower.png');

    });


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

  void _avatarMode()
  {
    print('avatorMode Function');
    //based on plant type
    setState(() {
      switch (_plantType) {
        case 5:
          {
            _mainImage = new Image.asset('assets/flower.png');
            _plantName = 'Default Flower';
          }
          break;
        case 1:
          {
            _mainImage = new Image.asset('assets/flower.png'); //todo update assets
          }
          break;
        case 2:
          {
            _mainImage = new Image.asset('assets/flower.png');
          }
          break;
        case 3:
          {
            _mainImage = new Image.asset('assets/flower.png');
          }
          break;
        case 4:
          {
            _mainImage = new Image.asset('assets/flower.png');
          }
          break;
      }
    });
  }

  void updateData()
  {
    print('avatorMode Function');
    //based on plant type
    setState(() {
      switch (_plantType) {
        case 5:
          {
            _mainImage = new Image.asset('assets/flower.png');
            _plantName = 'No Plant';
            _waterLevel = 0.0;
            _humidity = 0.0;
            _temperature = 0.0;
          }
          break;
        case 1:
          {
            _plantName = 'Violet';
            _waterLevel = 45.6;
            _humidity = 58.3;
            _temperature = 27.1;
          }
          break;
        case 2:
          {
            _plantName = 'Cactus';
            _waterLevel = 29.4;
            _humidity = 18.2;
            _temperature = 37.4;
          }
          break;
        case 3:
          {
            _plantName = 'Flower';
            _waterLevel = 44.1;
            _humidity = 39.7;
            _temperature = 34.5;
          }
          break;
        case 4:
          {
            _plantName = 'Grass';
            _waterLevel = 52.1;
            _humidity = 50.0;
            _temperature = 25.3;
          }
          break;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      appBar: AppBar(
          title: Text('Plant Type: ' + '$_plantName'),
          actions: <Widget>[
            // action button
            IconButton(
              icon: new Image.asset('assets/Logo.png'),
              onPressed: () { //set to avatar mode
                _avatarMode();
              },
            ),
            // action button
            IconButton(
              icon: Icon(Icons.videocam),
              onPressed: () { // set to video mode
                _videoReceiver();
              },
            ),
          ]
      ),

      body: Center(

        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Divider(
              height: 10,
            ),

            new FlatButton( //main image
              onPressed: _todo,
              child: _mainImage,
            ),

            Divider(
              height: 30,
            ),
            //List of plant data
            Row( //heading
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    'Metric: ',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    'Current:',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    'Ideal:',
                    style: Theme.of(context).textTheme.display1,
                  ),
                ]
            ),

            Row( //water
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    'Water:      ',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    '$_waterLevel',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    '$_idealWaterLevel',
                    style: Theme.of(context).textTheme.display1,
                  ),
                ]
            ),

            Row( //temp
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    'Temp:      ',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    '$_temperature',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    '$_idealTemperature',
                    style: Theme.of(context).textTheme.display1,
                  ),
                ]
            ),

            Row( //humidity
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    'Humidity:',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    '$_humidity',
                    style: Theme.of(context).textTheme.display1,
                  ),
                  Text(
                    '$_idealHumidity',
                    style: Theme.of(context).textTheme.display1,
                  ),
                ]
            ),

            Divider(
              color: Colors.green,
              thickness: 6,
              height: 30,
            ),
            Row( //Row of control buttons
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  FloatingActionButton(
                    onPressed: () => _sendCommand('00010000'),
                    tooltip: 'Water 1',
                    child: Icon(Icons.wb_cloudy),
                    backgroundColor: Colors.blueAccent,
                    foregroundColor: Colors.indigo,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00010001),
                    tooltip: 'Water 2',
                    child: Icon(Icons.wb_cloudy),
                    backgroundColor: Colors.blueAccent,
                    foregroundColor: Colors.indigo,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00010010),
                    tooltip: 'Water 3',
                    child: Icon(Icons.wb_cloudy),
                    backgroundColor: Colors.blueAccent,
                    foregroundColor: Colors.indigo,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00010011),
                    tooltip: 'Water 4',
                    child: Icon(Icons.wb_cloudy),
                    backgroundColor: Colors.blueAccent,
                    foregroundColor: Colors.indigo,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00010100),
                    tooltip: 'Water 5',
                    child: Icon(Icons.wb_cloudy),
                    backgroundColor: Colors.blueAccent,
                    foregroundColor: Colors.indigo,
                  ),


                ]
            ),
            Row( //Row of control buttons
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00100000),
                    tooltip: 'Brightness 1',
                    child: Icon(Icons.brightness_3),
                    backgroundColor: Colors.black,
                    foregroundColor: Colors.blueGrey,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00100001),
                    tooltip: 'Brightness 2',
                    child: Icon(Icons.brightness_2),
                    backgroundColor: Colors.black45,
                    foregroundColor: Colors.white30,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00100010),
                    tooltip: 'Brightness 3',
                    child: Icon(Icons.brightness_1),
                    backgroundColor: Colors.black26,
                    foregroundColor: Colors.white,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00100011),
                    tooltip: 'Brightness 4',
                    child: Icon(Icons.brightness_4),
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.deepOrange,
                  ),
                  FloatingActionButton(
                    onPressed: () => _sendCommand(00100100),
                    tooltip: 'Brightness 5',
                    child: Icon(Icons.brightness_5),
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.red,
                  ),

                ]
            ),
          ],
        ),
      ),
    );
  }


}
