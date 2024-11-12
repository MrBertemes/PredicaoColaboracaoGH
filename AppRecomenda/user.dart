import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:recomenda/main.dart';
import 'package:url_launcher/url_launcher.dart';

class User extends StatefulWidget {
  final String egresso;
  final String index;

  const User({super.key, required this.egresso, required this.index});

  @override
  State<User> createState() => _UserState();
}

class _UserState extends State<User> {
  late Future<Map<String, dynamic>> egressoFuture;

  Future<Map<String, dynamic>> fetchEgresso(String egresso) async {
    var client = http.Client();
    var urlReq = "$url/pred/$egresso"; // Substitua com sua URL
    var response = await client.get(Uri.parse(urlReq));
    var rb = json.decode(response.body) as Map<String, dynamic>;
    return rb;
  }

  Future<void> _launchURL(String url) async {
    if (!await launchUrl(Uri.parse(url))) {
      throw 'Could not launch $url';
    }
  }

  @override
  void initState() {
    super.initState();
    egressoFuture = fetchEgresso(widget.egresso);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: egressoFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(
            child: CircularProgressIndicator(
              strokeWidth: 5,
              color: Colors.red[900],
            ),
          );
        } else if (snapshot.hasError) {
          return Center(
            child: Text('Error: ${snapshot.error}'),
          );
        } else if (snapshot.hasData) {
          List<dynamic> colabs = snapshot.data!["pred"];
          return AlertDialog(
            contentPadding: const EdgeInsets.all(16.0),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Text(
                    "Egresso ${widget.index}",
                    style: TextStyle(
                      color: Colors.green[900],
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      "Talvez você gostaria de colaborar com esses usuários:",
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.green[800],
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  colabs.isNotEmpty
                      ? Wrap(
                          spacing: 8.0,
                          runSpacing: 8.0,
                          children: List.generate(
                            colabs.length < 5 ? colabs.length : 5,
                            (index) {
                              final recommendation = colabs[index][1];
                              final indexNome = "Usuário $index";
                              return GestureDetector(
                                onTap: () async {
                                  await _launchURL(
                                      "https://github.com/$recommendation");
                                },
                                child: Chip(
                                  label: Text(
                                    indexNome,
                                    style: TextStyle(color: Colors.red[900]),
                                  ),
                                  avatar: Icon(
                                    Icons.person_outline_rounded,
                                    color: Colors.red[900],
                                  ),
                                  backgroundColor: Colors.grey[200],
                                ),
                              );
                            },
                          ),
                        )
                      : const Text(
                          "Não há recomendações...",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.green,
                          ),
                        ),
                ],
              ),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('Fechar'),
              ),
            ],
          );
        } else {
          return const Center(
            child: Text('Sem dados disponíveis'),
          );
        }
      },
    );
  }
}
