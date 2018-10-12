'use strict';

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
    });



    
    


   
        
        
    