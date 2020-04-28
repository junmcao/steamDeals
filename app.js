const express = require('express');
const routes = require('./routes/index');
const path = require('path');
const bodyParser = require('body-parser');
const session = require('express-session');

const app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');


app.use(bodyParser.urlencoded({extended: true}));
app.use(express.json());
app.use(session({
    name: 'sid',
    cookie: {
        maxAge: 1000 * 60 * 60 *12,
        sameSite: true,
    },
    resave: false,
    saveUninitialized: false,
    secret: "secret-key"
}));
app.use('/', routes);
module.exports = app;
