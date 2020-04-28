const mongoose = require('mongoose');
var Schema = mongoose.Schema;

const gamesSchema = new Schema({
    _id: {
        type: mongoose.ObjectId,
    },
    title: {
        type: String,
        trim: true,
    },
    link: {
        type: String,
        trim: true,
    },
    original: {
        type: Number,
        trim: true,
    },
    sale: {
        type: Number,
        trim: true,
    },
    discount: {
        type: Number,
        trim: true,
    },
    currency: {
        type: String,
        trim: true,
    },
    date: {
        type: String,
        trim: true,
    },
    time: {
        type: String,
        trim: true,
    }
});

var Game = mongoose.model('games', gamesSchema);
module.exports = Game;