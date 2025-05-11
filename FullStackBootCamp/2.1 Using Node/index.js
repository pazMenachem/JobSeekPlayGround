import express from "express";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url))
const app = express()
const port = 3000;

app.use((req, res, next) => {
    console.log("MiddleWare 2!")
    next()
})

app.use((req, res, next) => {
    console.log("MiddleWare 1!")
    next()
})


app.get("/", (req, res) => {
    console.log("Received Get /")
    res.status(200).sendFile(join(__dirname, "public", "index.html"));
});

app.get("/test", (req, res) => {
    console.log("Received Get /test")
    res.status(200).send(req.body);
});

app.listen(port, () => {
   console.log(`Running on Port ${port}`) 
});