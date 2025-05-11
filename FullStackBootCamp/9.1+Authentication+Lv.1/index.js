import express from "express";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import { gracefulShutdown } from "./utils.js";
import { setupRoutes } from "./routes.js";
import session from "express-session";
import passport from "passport";
import { Strategy } from "passport-local";
import { googleVerify, localVerify } from "./controllers/authController.js";
import GoogleStrategy from 'passport-google-oauth2'

dotenv.config();
const app = express();
const port = process.env.PORT_SERVER || 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));
app.use(session({
      secret: process.env.SECRET_WORD,
      resave: false,
      saveUnitialized: true,
      cookie: {
        maxAge: 1000 * 60 * 15 // 15 minutes session
      }
  })
);

app.use(passport.initialize());
app.use(passport.session());

passport.use('local', new Strategy(localVerify));

passport.use(
  'google', 
  new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: 'http://localhost:3000/auth/google/secrets',
  userProfileURL: 'https://www.googleapis.com/oauth2/v3/userinfo'
  },
  googleVerify
));

passport.serializeUser((user, cb) => {
  cb(null, user);
});
passport.deserializeUser((user, cb) => {
  cb(null, user);
});


process.on("SIGINT", () => gracefulShutdown("SIGINT"));
process.on("SIGTERM", () => gracefulShutdown("SIGTERM"));
process.on("uncaughtException", (err) => gracefulShutdown("uncaughtException", err));

app.listen(port, async () => {
  try{
    setupRoutes(app);
    console.log(`Server running on port ${port}`);
  }
  catch (err){
    console.error(`DB connection issue: ${err.message}`)
  }
});
