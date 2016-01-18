/* jshint undef: false, unused: true */
"use strict";

var alexa = require("alexa-app");

// Allow this module to be reloaded by hotswap when changed
module.change_code = 1;

// Define an alexa-app
var app = new alexa.app("jarvis");
app.launch(function(req,res) {
	res.say("Hello, I am jarvis, how may I help you.");
});


app.intent("NameIntent", {
		     "slots": {"NAME": "LITERAL"},
		     "utterances": ["{Start the game|start|play} {fifa sixteen|black ops three|NAME}"]
	       },function(req, res) {              
		      res.say("Starting the game, "+req.slot("NAME")+" ");
		      res.say("<break time=\"1s\"/> PlayStation <break time=\"2s\"/>, "+req.slot("NAME")+" <break time=\"2s\"/> start");
	}
);

module.exports = app;
exports.handler = app.lambda();