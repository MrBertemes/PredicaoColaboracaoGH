// ignore_for_file: deprecated_member_use

import 'package:expansion_tile_card/expansion_tile_card.dart';
import 'package:flutter/material.dart';
import 'package:recomenda/grafo.dart';
import 'package:recomenda/user.dart';

String url = "http://10.0.2.2:8000";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recomendações',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Recomendando Colaborações'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final ScrollController scroll = ScrollController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Scrollbar(
        controller: scroll,
        child: CustomScrollView(
          controller: scroll,
          slivers: [
            SliverList(
              delegate: SliverChildBuilderDelegate(
                childCount: info.length,
                (context, index) {
                  final GlobalKey<ExpansionTileCardState> cardKey = GlobalKey();
                  var egressos = info.keys.toList();
                  var repos = info[egressos[index]]?.keys.toList();
                  num colabRecebidas = 0;
                  for (var colab in grafo[egressos[index]].values.toList()) {
                    colabRecebidas = colabRecebidas + colab;
                  }
                  return Padding(
                    padding: index == 0
                        ? const EdgeInsets.only(
                            top: 32,
                            bottom: 16,
                            right: 16,
                            left: 16,
                          )
                        : const EdgeInsets.all(16),
                    child: ExpansionTileCard(
                      key: cardKey,
                      title: Text(
                        "Egresso - ${(index + 1).toRadixString(16).toUpperCase()}",
                        style: const TextStyle(
                          fontSize: 20,
                          color: Colors.black,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      children: [
                        const Divider(
                          thickness: 1.0,
                          height: 1.0,
                        ),
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Padding(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 16.0,
                              vertical: 8.0,
                            ),
                            child: Text(
                              "Repositórios: ${repos?.length}",
                              style: Theme.of(context)
                                  .textTheme
                                  .bodyMedium!
                                  .copyWith(fontSize: 16),
                            ),
                          ),
                        ),
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Padding(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 16.0,
                              vertical: 8.0,
                            ),
                            child: Text(
                              "Colaborações Recebidas: $colabRecebidas",
                              style: Theme.of(context)
                                  .textTheme
                                  .bodyMedium!
                                  .copyWith(fontSize: 16),
                            ),
                          ),
                        ),
                        FittedBox(
                          fit: BoxFit.contain,
                          child: ButtonBar(
                            alignment: MainAxisAlignment.spaceBetween,
                            buttonHeight: 52.0,
                            buttonMinWidth: 90.0,
                            children: [
                              Row(
                                children: [
                                  TextButton(
                                    child: const Column(
                                      children: <Widget>[
                                        Icon(
                                          Icons.people_alt_rounded,
                                          color: Colors.red,
                                        ),
                                        Padding(
                                          padding: EdgeInsets.symmetric(
                                              vertical: 2.0),
                                        ),
                                        FittedBox(
                                          fit: BoxFit.contain,
                                          child: Text(
                                            'Recomendações',
                                            style: TextStyle(
                                              color: Colors.red,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    onPressed: () async {
                                      await showDialog(
                                        context: context,
                                        builder: (context) {
                                          return Scaffold(
                                            backgroundColor: Colors.transparent,
                                            body: User(
                                              egresso: egressos[index],
                                              index: (index + 1)
                                                  .toRadixString(2)
                                                  .toUpperCase(),
                                            ),
                                          );
                                        },
                                      );
                                    },
                                  ),
                                ],
                              )
                            ],
                          ),
                        )
                      ],
                    ),
                  );
                },
              ),
            )
          ],
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
