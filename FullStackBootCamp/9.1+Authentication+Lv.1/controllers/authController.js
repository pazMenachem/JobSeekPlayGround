import { getDB } from '../db.js';
import dotenv from 'dotenv'
import passport from 'passport';
import bcrypt from 'bcrypt';

dotenv.config();
const saltRounds = process.env.SALTROUNDS || 2

const db = await getDB();

/**
 * Renders the secrets page if the user is authenticated.
 * Redirects to the login page if the user is not authenticated.
 *
 * @param {request} req - The request object, containing user session and authentication status.
 * @param {Response} res - The response object, used to render views or redirect.
 */
export const getSecretsPage = async (req, res) => {
  if (req.isAuthenticated()) res.render('secrets.ejs');
  else res.send("User not Authenticated.");
};

export const loginLocalUser = passport.authenticate('local', {
  successRedirect: '/secrets',
  failureRedirect: '/'
});

export const loginGoogleUser = passport.authenticate("google", {
  scope: ['profile', 'email']
})

export const logout = async (req, res) => {
  req.logout((err) => {
    if (err) console.log(err);
    res.redirect("/");
  });
}

export const registerUser = async (req, res) => {
  const [email, password] = [req.body.username, req.body.password];
  
  try {
    const hashedPass = await bcrypt.hash(password, saltRounds);
    
    const user = await db.query(
      `INSERT INTO users (email, password) VALUES($1, $2) RETURNING *`,
      [email, hashedPass]
    );
    req.login(user, (err) => {
        if (err) {
          console.error(`Login error: ${err.message}`)
          return res.redirect("/register.ejs")
        };
        return res.redirect('/secrets');
      });
  }
  catch (err) {
    console.log(`Failed to insert user: ${err.message}`);
    res.render("register.ejs");
  }
};


export const googleVerify = async (accessToken, refreshToken, profile, cb) => {
    try{
      const qRes = await db.query("select * from users where email=$1", [profile.email])
      if (qRes.rows.length === 0){
        const newUser = await db.query("insert into users (email, password) values ($1, $2) returning *", [profile.email, 'google']);
        cb(null, newUser.rows[0]);
      }
      else{
        cb(null, qRes.rows[0])
      }
  }
  catch(err){
      cb(err);
    }
};

/**
 * Verifies user credentials for Passport Local Strategy.
 * 
 * @param {string} username - The email/username provided during login.
 * @param {string} password - The password provided during login.
 * @param {Function} cb - Passport callback to handle verification result.
 */
export const localVerify = async (username, password, cb) => {  
  const qRes = await db.query(
    `SELECT * FROM users WHERE email = $1`,
    [username]
  );
  
  try {
    const hashedPass = qRes.rows[0].password;
    bcrypt.compare(password, hashedPass, async (err, result) => {
      if (err) return cb(err);
      if (result) return cb(null, qRes.rows[0]); // Send back the user
      else return cb(null, false);
    });
  }
  catch (err) {
    console.log(`Failed to find user: ${err.message}`);
    return cb(err)
  }
};
