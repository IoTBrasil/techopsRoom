
var bodyParser = require('body-parser');

app.use(bodyParser.json());

app.post('/:temp', function (req, res) {	
	console.log('Temperatura: ', req.body.status)
});
