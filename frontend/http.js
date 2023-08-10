var http = require("http")
http.createServer(function(requeast, response) {
  response.writeHead(200, {
    "Content-Type" : "text/plain;charset=utf-8"
  });
  response.write("hello world");
  response.end();
}).listen(10000);
console.log("start");