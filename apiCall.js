/*
var http = require("http");
var options = {
  hostname: '127.0.0.1',
  port: 8000,
  path: '/phantom/submitMessage',
  method: 'POST',
  headers: {
      'Content-Type': 'application/json',
  }
};
var req = http.request(options, function(res) {
  console.log('Status: ' + res.statusCode);
  console.log('Headers: ' + JSON.stringify(res.headers));
  res.setEncoding('utf8');
  res.on('data', function (body) {
    console.log('Body: ' + body);
  });
});
req.on('error', function(e) {
  console.log('problem with request: ' + e.message);
});
// write data to request body

req.write(String(requestDict));
req.end();
*/
  
var callDjangoAPI = function(requestBody, url, cb) {
  var request = require('request');
  request.post(
      url,
      { json: requestBody },
      function (error, response, body) {
          if (!error && response.statusCode == 200) {
              cb(body);
          }
      }
  );
}

module.exports.callDjangoAPI = callDjangoAPI;

