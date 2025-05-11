import passport from 'passport';
import {
    registerUser,
    loginLocalUser, 
    loginGoogleUser, 
    getSecretsPage,
    logout
} from './controllers/authController.js';

export const setupRoutes = (app) => {
  app.get("/", (req, res) => res.render("home.ejs"));
  app.get("/login", (req, res) => res.render("login.ejs"));
  app.get("/register", (req, res) => res.render("register.ejs"));
  app.get("/secrets", getSecretsPage);
  app.get("/auth/google", loginGoogleUser);
  app.get("/logout", logout);

  app.get("/auth/google/secrets", passport.authenticate("google", {
    successRedirect: "/secrets",
    failureRedirect: "/login"
  }));

  app.post("/register", registerUser);
  app.post("/login", loginLocalUser);
}; 