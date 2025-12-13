import { fetchAppBySlug, fetchApps, fetchAppSSById } from "./NODEJS/db.js";
import express from 'express'
import cors from "cors";
const app = express()

app.use(cors({
  origin: "http://localhost:4321"
}));

// app.use(cors())

app.get("/api/apps",async(req, res)=>{
const apps = await fetchApps("apps")
console.log(apps);

res.send(apps)

})

app.get("/api/blogs",async(req, res)=>{
const apps = await fetchApps("blogs")
res.send(apps)

})


app.get("/api/app/:app_name", async (req, res) => {
  // http://localhost:5000/api/app/1319636
  const app_name = req.params.app_name;
  if (!app_name) {
    return res.status(400).json({ error: "Invalid ID" });
  }

  try {
    const app = await fetchAppBySlug(app_name);
    console.log(app);
    
    if (!app) {
      return res.status(404).json({ error: "App not found", app_name });
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



app.get("/api/app/download/:app_id", async(req, res)=>{
  const app_id = req.params.app_id
  console.log('downlloading...: ',app_id);
  res.json({"msg":"downladiing","satus":"ok","app_id":app_id})
})



app.listen(8000, () => {
  console.log("running...");
});
