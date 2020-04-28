require('dotenv').config();

const mongoose = require('mongoose');

const port = process.env.PORT || 8080;
mongoose.connect(process.env.DATABASE, {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

mongoose.connection
    .on('open', ()=>{
        console.log('Mongoose connection open');
    })
    .on('error', (err)=>{
        console.log("Connection error: ${err.message}");
    });

    require('./models/register');
    require('./models/games');
const app = require('./app');
const server = app.listen(port, ()=>{
    console.log('Express is running on port ${server.address().port}');
});
