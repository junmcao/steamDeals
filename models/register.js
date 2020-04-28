const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
var Schema = mongoose.Schema;

const registerSchema = new Schema({
    uname: {
        type: String,
        trim: true,
    },
    email: {
        type: String,
        trim: true,
    },
    password: {
        type:String,
        trim: true,
    },
    savedDeals: {
        type: [String],
        trim: true,
    }
});

//hash password
registerSchema.methods.generateHash = function(password){
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

//check if password is valid
registerSchema.methods.validPassword = function(password){
    return bcrypt.compareSync(password, this.password);
};

var User = mongoose.model('user', registerSchema);
module.exports = User;