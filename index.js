'use strict';
    var apiCall = require("./apiCall");

    var Botkit = require('botkit');
    var request = require('request');

    var controller = Botkit.slackbot({
        retry: true,
        debug: false
    });

    var theConnectionsDict = {};


    // connect the bot to a stream of messages
    function createConnection(accessToken, teamId) {
        var myBot = controller.spawn({
            retry: true,
            token: accessToken,
        }).startRTM();
        theConnectionsDict[teamId] = myBot;
    }


    var teamId = "TCZ7MEPNW"
    var accessToken = "xoxb-441259499778-441069992868-Nx4VQr9OWa3jHSpsB6rH6uy3"
    var baseUrl = "http://0.0.0.0:8000/"
    createConnection(accessToken, teamId)

    controller.hears('help', ['direct_message','direct_mention','mention'],function(bot,message) {
        console.log('here');
        theConnectionsDict[teamId].reply(message, "Hi");
    });

    controller.hears('(.*)', ['direct_message','direct_mention','mention'],function(bot,message) {
                var requestDict = {};
        requestDict["message"] = message;
        var channelId = message["channel"]
        var apiUrl = baseUrl + "messages/send";
        apiCall.callDjangoAPI(requestDict, apiUrl, function(response){
            theConnectionsDict[teamId].reply(message, response);
        });

    });

    var express = require("express");
    var myParser = require("body-parser");
    var qs = require('qs')
    var app = express();
    app.use(myParser.urlencoded({extended : true}));
    app.use(myParser.json());

    app.post("/notify/channels", function(request, res) {
        console.log(request.body);
        var channels = request.body['channels'];
        var message = request.body['message'];
        var teamId = request.body['team']
        var attachments = undefined;
        for (var i = 0; i < channels.length; i++) {
            theConnectionsDict[teamId].say({
                text: message,
                attachments: attachments,
                channel: channels[i]
            });
        }
    });

    app.post("/slack/interaction", function(request, res) {
       var theOuterDict = qs.parse(request.body);
       var thePayloadDict = JSON.parse(theOuterDict['payload']);
       var apiURL = baseUrl + 'messages/slack/interaction';
       apiCall.callDjangoAPI(thePayloadDict, apiURL, function(response) {
            res.status(200).send("You can now start learning!");
       }
        );
    });

    app.listen(3000);









