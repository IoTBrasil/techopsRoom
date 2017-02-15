'use strict';

let client = '../client'
let path = require('path')
let app = require('express')()
let server = require('serve-static')
let config = require('config').server
let http = require('http').Server(app)

app.use('/', server(path.resolve(__dirname, client)))

app.get('/api/:temp', function (req, res) {	
	console.log('Temperatura: ', req.body.status)
});

http.listen( config.port , function () {
  console.log('Server listening at port %d', config.port );
});
