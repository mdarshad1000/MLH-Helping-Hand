const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Hello World, from express');
});

app.use(cors());

// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

let restrolist= [];

app.post('/book', (req, res) => {
    const restro = req.body;

    // Output the book to the console for debugging
    console.log(restro);
    restrolist.push(restro);

    res.send('Restaurant is added to the database');
});

app.get('/books', (req, res) => {
    res.json(restrolist);
});

app.listen(port, () => {
  console.log(`Twilio App litening on port ${port}`)
})