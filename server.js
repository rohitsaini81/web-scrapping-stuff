import { fetchAppById, fetchApps, fetchAppSSById } from "./NODEJS/db.js";
import express from 'express'

const app = express()


app.get("/api/apps",async(req, res)=>{
const apps = await fetchApps("apps")
console.log(apps);

res.send(apps)

})

app.get("/api/blogs",async(req, res)=>{
const apps = await fetchApps("blogs")
res.send(apps)

})


app.get("/api/app/:id", async (req, res) => {
  // http://localhost:5000/api/app/1319636
  const id = req.params.id;

  if (!id || isNaN(id)) {
    return res.status(400).json({ error: "Invalid ID" });
  }

  try {
    const app_id = parseInt(id)
    const app = await fetchAppById(app_id);

    if (!app) {
      return res.status(404).json({ error: "App not found", id });
    }

    return res.json(app);  // ALWAYS return JSON
  } catch (error) {
    console.error("API ERROR:", error);
    return res.status(500).json({ error: "Server error" });
  }
});


app.get("/api/app/screenshots/:id", async(req, res)=>{
const id = req.params.id;

  if (!id || isNaN(id)) {
    return res.status(400).json({ error: "Invalid ID" });
  }

  try {
    const app_id = parseInt(id)
    const app = await fetchAppSSById(app_id);

    if (!app) {
      return res.status(404).json({ error: "App ScreenShot not found", id });
    }

    return res.json(app);  // ALWAYS return JSON
  } catch (error) {
    console.error("API ERROR:", error);
    return res.status(500).json({ error: "Server error" });
  }

    
})




app.listen(5000,()=>{
console.log("running...")})
