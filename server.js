import { fetchApps } from "./NODEJS/db.js";
import express from 'express'

const app = express()


app.get("/api/apps",async(req, res)=>{
const apps = await fetchApps("app")
res.send(apps)

})


app.listen(5000,()=>{
console.log("running...")})
