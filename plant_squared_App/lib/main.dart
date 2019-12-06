import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:convert';



/*
Project Group T5
Plant Squared
Main developer: Jerry Xiong

App for Monitoring and Controlling a plant

Display:
Name of Type of Plant
Ideal: water, temperature and humidity
Current: water, temperature and humidity

Actions:
Refresh data
Water Plant (5 levels)
Adjust Light (5 levels)

 */


//....................................
//      Global Variables
//....................................
// App connection set up
var phoneIP = new InternetAddress('192.168.43.105');
var phonePort = 9003;

// Server connection set uo
var serverIP = new InternetAddress('192.168.43.129');
var serverPort = 8001;

// Encoded Responses
var ACK = '01100001';
var NACK = '01101110';
var UPDATE = '01110000';

var WATER1 = '00010001';
var WATER2 = '00010010';
var WATER3 = '00010011';
var WATER4 = '00010100';
var WATER5 = '00010101';

var LIGHT1 = '00100000';
var LIGHT2 = '00100010';
var LIGHT3 = '00100011';
var LIGHT4 = '00100100';
var LIGHT5 = '00100101';

// Other Values
const textClearTime = 5; //text stays for 5 seconds before clearing


//main function runs the app
void main() {
  runApp(MyApp());
}

//App build
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

//Homepage
class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

//Configuration
class _MyHomePageState extends State<MyHomePage> {

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
  String _mainText;

  @override
  initState(){
    _mainImage = Image.asset('assets/Logo.png');
    _plantName = 'No Plant';
    _mainText = '  ';
  }
  //****************************************

  //Reset
  reset()
  {
    print('Reset Content');
    setState(() {
      _mainImage = new Image.asset('assets/Logo.png');
      _plantName = 'No Plant';
      _idealWaterLevel = 0.0;
      _idealHumidity = 0.0;
      _idealTemperature = 0.0;
      _waterLevel = 0.0;
      _humidity = 0.0;
      _temperature = 0.0;
      clearTextAfter();
    });
  }

  //Clearing the main text
  clearMainText()
  {
    setState(() {
      _mainText = '  ';
    });
  }

  //Allow the text to display for some time before clearing it
  Future clearTextAfter()
  {
    return new Future.delayed(const Duration(seconds: textClearTime), () => clearMainText());
  }

  //Send UPD packets based on user command is given
  void _sendCommand(String x) {
    print('send command function: '  + '$x');
    var codec = new Utf8Codec();
    List<int> dataToSend = codec.encode(x);
    print(dataToSend);

    RawDatagramSocket.bind(phoneIP, phonePort).then((RawDatagramSocket udpSocket) {
      udpSocket.send(dataToSend, serverIP, serverPort);
      print('Sent data on the stream...');

      //Waiting to receive data packet containing plant info or responses
      udpSocket.listen((e) {
        print(e.toString());
        Datagram dg = udpSocket.receive();
        if(dg != null){

          var codec = new Utf8Codec();
          String str = codec.decode(dg.data);
          print('Received Data = ');
          print(str);
          if(str.startsWith(ACK))
          {
            print('Received Ack ');
            _mainText = 'Command Received by Server';
            updateData();
            clearTextAfter();
          }
          else if(str.startsWith(NACK))
            {
              print('Received Nack ');
              _mainText = 'Command Not Recognized!';
              clearTextAfter();
            }
          else
            {
              try{ //Decode the message as a Json
                var parsedJson = json.decode(str);
                List<int> response = codec.encode(ACK);
                udpSocket.send(response, serverIP, serverPort);
                print('update data based on received json');
                setState(() {
                  _waterLevel = parsedJson['moisture'];
                  _temperature = parsedJson['temperature'];
                  _humidity = parsedJson['humidity'];
                  _plantType = parsedJson['plant_id'];
                  updateData();
                });
              } on FormatException catch (e){
                print('The message is not a valid json. Send back Nack');
                List<int> response = codec.encode(NACK);
                _mainText = 'Received bad data!';
                udpSocket.send(response, serverIP, serverPort);
              }
            }
        }
      });
    });
  }

  void updateData()
  {
    //based on plant type
    print('updating the data based on plant type');
    print(_plantType);
      switch (_plantType) {
        case 5: //No plant scenario
          {
            setState(() {
              _mainImage = new Image.asset('assets/Logo.png');
              _plantName = 'No Plant';
              _idealWaterLevel = 0.0;
              _idealHumidity = 0.0;
              _idealTemperature = 0.0;
              //_mainText = 'Plant Data Updated';
              clearTextAfter();
            });
          }
          break;
        case 1:
          {
            setState(() {
              _mainImage = new Image.asset('assets/cactus.png');
              _plantName = 'Cactus';
              _idealWaterLevel = 29.4;
              _idealHumidity = 18.2;
              _idealTemperature = 37.4;
              _mainText = 'Plant Data Updated';
              clearTextAfter();
            });
          }
          break;
        case 2:
          {
            setState(() {
              _mainImage = new Image.asset('assets/haworthiafasciata.png');
              _plantName = 'Zebra';
              _idealWaterLevel = 44.1;
              _idealHumidity = 39.7;
              _idealTemperature = 34.5;
              _mainText = 'Plant Data Updated';
              clearTextAfter();
            });
          }
          break;
        case 3:
          {
            setState(() {
              _mainImage = new Image.asset('assets/jade.png');
              _plantName = 'Jade';
              _idealWaterLevel = 52.1;
              _idealHumidity = 50.0;
              _idealTemperature = 25.3;
              _mainText = 'Plant Data Updated';
              clearTextAfter();
            });
          }
          break;
        case 4:
          {
            setState(() {
              _mainImage = new Image.asset('assets/africanviolet.jpg');
              _plantName = 'Flower';
              _idealWaterLevel = 52.1;
              _idealHumidity = 50.0;
              _idealTemperature = 25.3;
              _mainText = 'Plant Data Updated';
              clearTextAfter();
            });
          }
          break;
        default: {

          setState(() {
            _mainText = 'Received bad plant type';
            _plantName = 'No Plant';
            _mainImage = new Image.asset('assets/Logo.png');
            _idealWaterLevel = 0.0;
            _idealHumidity = 0.0;
            _idealTemperature = 0.0;
            clearTextAfter();
          });
          print('Received bad plant type = ');
          print(_plantType);
          print('Set to default');
        }
      }
  }

  //Main app Layout
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      appBar: AppBar(
          title: Text('Plant Type: ' + '$_plantName'),
          actions: <Widget>[
      // action button
            IconButton(
            icon: Icon(Icons.autorenew),
            onPressed: () { //set to avatar mode
              reset();
            },
    )]
    ),

      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Divider(
              color: Colors.green,
              thickness: 1,
              height: 1,
            ),

            new FlatButton( //main image
              onPressed: () => _sendCommand(UPDATE),
              child: _mainImage,
            ),

            Divider(
              color: Colors.green,
              thickness: 1,
              height: 1,
            ),
            //List of plant data

            Text(
              '$_mainText',
              style: Theme.of(context).textTheme.headline,
            ),

            Divider(
              color: Colors.green,
              thickness: 1,
              height: 1,
            ),
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
                    style: Theme.of(context).textTheme.headline,
                  ),
                  Text(
                    '$_waterLevel',
                    style: Theme.of(context).textTheme.headline,
                  ),
                  Text(
                    '$_idealWaterLevel',
                    style: Theme.of(context).textTheme.headline,
                  ),
                ]
            ),

            Row( //temp
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    'Temp:      ',
                    style: Theme.of(context).textTheme.headline,
                  ),
                  Text(
                    '$_temperature',
                    style: Theme.of(context).textTheme.headline,
                  ),
                  Text(
                    '$_idealTemperature',
                    style: Theme.of(context).textTheme.headline,
                  ),
                ]
            ),

            Row( //humidity
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    'Humidity:',
                    style: Theme.of(context).textTheme.headline,
                  ),
                  Text(
                    '$_humidity',
                    style: Theme.of(context).textTheme.headline,
                  ),
                  Text(
                    '$_idealHumidity',
                    style: Theme.of(context).textTheme.headline,
                  ),
                ]
            ),

            Divider(
              color: Colors.green,
              thickness: 1,
              height: 1,
            ),

            Container(
              color: Colors.lightBlueAccent,
              child: Row( //Row of control buttons for WATER
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    FloatingActionButton(
                      onPressed: () => _sendCommand(WATER1),
                      tooltip: 'Water 1',
                      child: new Tab(
                          icon: Container(
                              child: new Image.asset('assets/watericon1.png'),
                              height:20,
                              width: 20
                          )
                      ),
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.lightBlueAccent,
                    ),
                    FloatingActionButton(
                      onPressed: () => _sendCommand(WATER2),
                      tooltip: 'Water 2',
                      child: new Tab(
                          icon: Container(
                              child: new Image.asset('assets/watericon2.png'),
                              height:40,
                              width: 40
                          )
                      ),
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.blue,
                    ),
                    FloatingActionButton(
                      onPressed: () => _sendCommand(WATER3),
                      tooltip: 'Water 3',
                      child: new Tab(
                          icon: Container(
                              child: new Image.asset('assets/watericon3.png'),
                              height:40,
                              width: 40
                          )
                      ),
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.indigo,
                    ),
                    FloatingActionButton(
                      onPressed: () => _sendCommand(WATER4),
                      tooltip: 'Water 4',
                      child: new Tab(
                          icon: Container(
                              child: new Image.asset('assets/watericon4.png'),
                              height:40,
                              width: 40
                          )
                      ),

                      backgroundColor: Colors.white,
                      foregroundColor: Colors.black26,
                    ),
                    FloatingActionButton(
                      onPressed: () => _sendCommand(WATER5),
                      tooltip: 'Water 5',
                      child: new Tab(
                          icon: Container(
                              child: new Image.asset('assets/watericon5.png'),
                              height:40,
                              width: 40
                          )
                      ),
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.indigo,
                    ),
                  ]
              ),
            ),

        Container(
          color: Colors.yellowAccent[100],
          child: Row( //Row of control buttons for LIGHT
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                FloatingActionButton(
                  onPressed: () => _sendCommand(LIGHT1),
                  tooltip: 'Brightness 1',
                  child: Icon(Icons.brightness_3),
                  backgroundColor: Colors.black,
                  foregroundColor: Colors.blueGrey,
                ),
                FloatingActionButton(
                  onPressed: () => _sendCommand(LIGHT2),
                  tooltip: 'Brightness 2',
                  child: Icon(Icons.brightness_2),
                  backgroundColor: Colors.black45,
                  foregroundColor: Colors.white30,
                ),
                FloatingActionButton(
                  onPressed: () => _sendCommand(LIGHT3),
                  tooltip: 'Brightness 3',
                  child: Icon(Icons.brightness_1),
                  backgroundColor: Colors.black26,
                  foregroundColor: Colors.white,
                ),
                FloatingActionButton(
                  onPressed: () => _sendCommand(LIGHT4),
                  tooltip: 'Brightness 4',
                  child: Icon(Icons.brightness_4),
                  backgroundColor: Colors.white,
                  foregroundColor: Colors.deepOrange,
                ),
                FloatingActionButton(
                  onPressed: () => _sendCommand(LIGHT5),
                  tooltip: 'Brightness 5',
                  child: Icon(Icons.brightness_5),
                  backgroundColor: Colors.white,
                  foregroundColor: Colors.red,
                ),
              ]
          ),
        ),
          ],
        ),
      ),
    );
  }
}
