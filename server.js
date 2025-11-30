import { fetchApps } from "./NODEJS/db.js";



const apps = await fetchApps("app")
console.log(apps)