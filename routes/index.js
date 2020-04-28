const express = require('express');
const mongoose = require('mongoose');
const {check, validationResult} = require('express-validator');
const router = express.Router();
const path = require('path');
const auth = require('http-auth');
const User = mongoose.model('user');
const Game = mongoose.model('games');

const basic = auth.basic({
    file: path.join(__dirname, "../users.htpasswd"),
});


//check if logged in 

const checkLoggedIn=((req, res, next) => {
    if (req.session.loggedIn) {
        next();
    }
    else{
        res.redirect("/login");
    }
});

const checkNotLoggedIn=((req, res, next) =>{
    if (req.session.loggedIn){
        res.redirect("/");
    }
    else{
        next();
    }
});

//logs user out
router.get('/logout', (req,res) => {
    req.session.loggedIn= false;
    req.session.user=null;
    req.session.saves=null;
    res.redirect("/");
});


//home page displays first 20 games
router.get('/', (req,res) => {
    console.log(req.session);
    Game.find().limit(20)
        .then((games) => {
            // console.log(JSON.stringify(games));
            res.render('home', {title: 'Steam Deals', games});
        })
        .catch(() => {
            res.send("something went wrong");
        });
});


//renders register page 
router.get('/register', checkNotLoggedIn, (req,res) => {
    res.render('form', {title: 'Register'});
});

//when user submits register page then it will be added to the mongodb
router.post('/register', 
    [
        check('uname')
            .not().isEmpty()
            .trim()
            .escape()
            .withMessage("Please enter a username"),
        check('email')
            .isEmail()
            .normalizeEmail()
            .withMessage("Please enter a valid email address"),
        check('password')
            .isLength({min:5})
            .withMessage("Minimum length of 5 required"),
        check('confirmPassword')
            .isLength({min:5})
            .withMessage("Minimum length of 5 is required")
            .custom((value, {req}) => {
                if (value !== req.body.password){
                    console.log(value);
                    console.log(req.body.password);
                    throw new Error('Passwords do not match');
                }
                else{
                    return value;
                }
            })
    ],
    (req, res) => {
        const errors = validationResult(req);
        console.log(errors);
        if (errors.isEmpty()){
            var newUser = new User({
                uname: req.body.uname,
                email: req.body.email 
            });

            newUser.password = newUser.generateHash(req.body.password);
            newUser.save()
                .then(() => { 
                    console.log("Registration completed");
                    res.redirect('/login');
                })
                .catch((err) => {
                    console.log(err);
                    res.render('form', { title: 'Register' });
                });
        }
        else{
            res.render('form', {
                title: 'Register',
                errors: errors.array(),
                data: req.body
            })
        }
        // console.log(req.body);
        // res.render('form', { title: 'Register' });
});

//render login page
router.get('/login', checkNotLoggedIn, (req,res) => {
    res.render('login', {title: 'Login'});
});

//login
router.post('/login', (req, res) => {
    console.log(req.body.uname);
    console.log(req.body.password);
    User.findOne({uname: req.body.uname}, (err, user) => {
        console.log(user.password);
        console.log(user.uname);
        if (!user.validPassword(req.body.password)){
            console.log("Password did not match");
        }
        else{
            console.log("Successfully logged in!");
            req.session.loggedIn = true;
            req.session.user = user.uname;
            req.session.saves = user.savedDeals;
            console.log(req.session.saves);
            res.redirect('../');
        }
    });
});


//displays all saved games 
router.get('/saves', checkLoggedIn, (req, res) => {
    console.log(req.session.user + " is logged in");
    console.log(req.session.saves);
    var sesh = req.session;
    var savedGames =  [];
    if (sesh.saves.length){
        var gameCount = 0;
        for (x of sesh.saves){
            // console.log(x);
            Game.find({"title": x})
            .then((games) => {
                savedGames.push(games);
                gameCount++;
                // console.log(savedGames);
                if (gameCount==sesh.saves.length){
                    console.log(savedGames);
                    res.render('saves', {title: 'Saved games', sesh, savedGames});
                }
            })
            .catch(()=>{
                res.send("Something went wrong.");
            })
        }
    }
    else{
        res.render('saves', {title: 'Saved games', sesh});
    }
});

router.get('/remove?:title', checkLoggedIn, (req, res) =>{
    //update session
    console.log(req.session.saves);
    const index = req.session.saves.indexOf(req.query.title);
    if (index >-1){
        req.session.saves.splice(index, 1);
    }
    console.log(req.session.saves);
    
    req.session.save();
    //remove from mongodb
    User.updateOne({"uname": req.session.user}, {$set: {"savedDeals": req.session.saves}})
        .then(()=>{
            console.log("Success!")
            res.redirect('/saves');
        })
        .catch(()=>{
            console.log("Failed");
        })
});

//saves games to session then writes to db
router.get('/save?:title', checkLoggedIn, (req, res) =>{
    req.session.saves.push(req.query.title);
    console.log(req.session.saves);
    req.session.save();

    //save to mongodb
    User.updateOne({"uname": req.session.user}, {$push: {"savedDeals": req.query.title}})
        .then(() => {
            console.log("Success!");
        })
        .catch(() => console.log("Failed"));

});
//secret page with all registered users and their hashed passwords
router.get('/registrations', (req, res) => {
    User.find()
        .then((users) => {
            console.log(users);
            res.render('index', {title: 'Listing users', users});
        })
        .catch(() => { res.send("Something went wrong.");});
});

//gets games through search query
router.get('/search?:title', check('title').not().isEmpty(),(req, res) =>{
    const errors = validationResult(req);
    console.log(errors);
    if (errors.isEmpty()){
        console.log("title is " + req.query.title);
        Game.find({"title": {'$regex': req.query.title, "$options": "i"}})
            .then((games) => {
                console.log(games);
                res.render('search', {title: 'Search', games});
            }) 
            .catch(() => {
                res.send("Something went wrong.");
            });
    }
});
module.exports = router;