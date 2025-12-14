
import axios from 'axios';
import * as cheerio from 'cheerio';
import FormData from 'form-data'
import pool, { fetchApps } from "./NODEJS/db.js"

async function fetchUptoDownApi(url1) {
  const form = new FormData();
  form.append("page", "2");
  try {

    const response = await axios.post(url1, form, {
      headers: form.getHeaders()
    })
    return response.data
  }
  catch (err) {
    throw new Error(err);

  }
}


async function getFinalDownloadLink(appUrl) {
  try {
    // STEP 1 — Load main app page
    const page = await axios.get(appUrl);
    const $ = cheerio.load(page.data);

    // STEP 2 — Extract the download page link
    const downloadPageUrl = $("#button-download-page-link").attr("href");

    if (!downloadPageUrl) {
      throw new Error("Download page URL not found.");
    }

    // console.log("Download page:", downloadPageUrl);

    // STEP 3 — Load the download page and extract token
    const downloadPage = await axios.get(downloadPageUrl);
    const $$ = cheerio.load(downloadPage.data);

    const token = $$("#detail-download-button").data("url");

    if (!token) {
      throw new Error("Download token not found.");
    }

    // console.log("Token:", token);

    // Build the redirect URL exactly like the browser iframe does
    const iframeUrl = "https://dw.uptodown.net/dwn/" + token;

    // console.log("Redirect URL:", iframeUrl);

    // STEP 4 — Follow redirects to get the FINAL download link
    const final = await axios.get(iframeUrl, {
      maxRedirects: 10,
      validateStatus: () => true, // allow redirects
    });

    const finalUrl = final.request.res.responseUrl;
    console.log(finalUrl);
    
    return finalUrl;
    // console.log("\n🔥 FINAL DIRECT DOWNLOAD LINK:");
    // console.log(finalUrl);

  } catch (err) {
    console.error("Error:", err.message);
  }
}

// getFinalDownloadLink("https://tiktok-lite.en.uptodown.com/android"); //.apk url




async function getlistofApps(pageUrl) {
  try {
    const page = await axios.get(pageUrl);
    const $ = cheerio.load(page.data);

    // STEP 2 — Extract the download page link
    const page_data = $(".content")[1]
    const $$ = cheerio.load(page_data)

    const items = $$(".item")
    items.map((index, e) => {
      const $$$ = cheerio.load(e)
      console.log(index)
      // const app_obj={
      //   href_url:e.attribs.onclick.split(";")[0].split("=")[1],
      //   app_name:$$$(".name").children("a").text(),
      //   description:$$$(".description").text(),
      //   image_link:$$$("figure").children().attr().src
      // }
      console.log(e)
      // console.log($$$(".name").children("a").text());
      // console.log($$$(".description").text());
      // console.log($$$("figure").children().attr().src);

    })
  } catch (error) {
    console.log(error)
  }
}
// getlistofApps("https://en.uptodown.com/android/apps")






async function scrapeUptodown(url) {
  const pageHtml = await axios.get(url)
  const $ = cheerio.load(pageHtml.data);

  const data = {};

  // --- BASIC INFO ---
  data.name = $("#detail-app-name").text().trim();
  data.version = $(".info .version").first().text().trim();
  data.author = $("#author-link, #author-link-ofuscated").text().trim();

  // --- RATING / REVIEWS ---
  data.rating = $("#rating-inner-text").text().trim();
  data.reviews = $("#show-comments_app span").first().text().trim();

  // --- DOWNLOADS ---
  data.downloads = $(".dwstat span").first().text().trim();

  // --- LAST UPDATED ---
  data.lastUpdated = $("#button-download-page-link p:nth-of-type(2)").text().trim();

  // --- MAIN DESCRIPTION ---
  data.description = $(".text-description").text().trim();

  // --- PACKAGE NAME ---
  data.packageName = $("th:contains('Package Name')").next("td").text().trim();

  // --- CATEGORY ---
  data.category = $("th:contains('Category')")
    .next("td")
    .find("a")
    .text()
    .trim();

  // --- REQUIREMENTS ---
  data.requirements = $(".requirements li").map((i, el) => $(el).text().trim()).get();

  // --- SCREENSHOTS ---
  data.screenshots = $(".gallery picture img")
    .map((i, el) => $(el).attr("src"))
    .get();

  // --- OLDER VERSIONS ---
  data.olderVersions = $("#versions-items-list > div").map((i, el) => ({
    type: $(el).find(".type").text().trim(),
    version: $(el).find(".version").text().trim(),
    sdk: $(el).find(".sdkVersion").text().trim(),
    date: $(el).find(".date").text().trim(),
    url: $(el).attr("data-url"),
    versionId: $(el).attr("data-version-id")
  })).get();

  // --- DOWNLOAD URL ---
  data.downloadUrl = $("#button-download-page-link").attr("href");

  return data;
}


function buildSqlQuery(table, data) {
  const columns = Object.keys(data);
  const values = Object.values(data);

  // PostgreSQL uses $1, $2, $3 placeholders
  const placeholders = columns.map((_, idx) => `$${idx + 1}`);

  const sql = `
    INSERT INTO ${table} (${columns.join(", ")})
    VALUES (${placeholders.join(", ")})
    RETURNING *;
  `;

  return { sql, values };
}


function buildAppSql(app_id, app_info) {
  const esc = (v) => typeof v === "string" ? v.replace(/'/g, "''") : v;

  const rating = Number(app_info.rating) || 0;
  const reviews = Number(app_info.reviews) || 0;
  const downloads = Number(app_info.downloads) || 0; // <-- fix here

  const appSql = `
INSERT INTO app (
  name, version, author, rating, reviews, downloads, last_updated,
  description, package_name, category, requirements
) VALUES (
  '${esc(app_info.name)}',
  '${esc(app_info.version)}',
  '${esc(app_info.author)}',
  ${rating},
  ${reviews},
  ${downloads},
  '${new Date(app_info.lastUpdated).toISOString().split("T")[0]}',
  '${esc(app_info.description)}',
  '${esc(app_info.packageName)}',
  '${esc(app_info.category)}',
  ARRAY[${app_info.requirements.map(r => `'${esc(r)}'`).join(", ")}]
)
RETURNING id;`.trim();

  const screenshotsSql = app_info.screenshots.map(url => `
INSERT INTO app_screenshots (app_id, url)
VALUES (${app_id}, '${esc(url)}');`.trim()
  ).join("\n");

  const versionsSql = app_info.olderVersions.map(v => `
INSERT INTO app_versions (app_id, type, version, sdk, release_date, url, version_id)
VALUES (
  ${app_id},
  '${esc(v.type)}',
  '${esc(v.version)}',
  '${esc(v.sdk)}',
  '${new Date(v.date).toISOString().split("T")[0]}',
  '${esc(v.url)}',
  '${esc(v.versionId)}'
);`.trim()
  ).join("\n");

  return { appSql, screenshotsSql, versionsSql };
}


export async function findApp(appId) {
  const client = await pool.connect();

  try {
    const result = await client.query(
      "SELECT * FROM apps WHERE id = $1;",
      [appId]
    );

    if (result.rows.length === 0) {
      return null;
    }

    // rows[0] === data[0] in Python
    return result.rows[0];

  } catch (err) {
    console.error("Error finding app:", err);
    throw err;
  } finally {
    client.release();
  }
}

export async function findAppConent(appId) {
  const client = await pool.connect();

  try {
    const result = await client.query(
      "SELECT * FROM app WHERE id = $1;",
      [appId]
    );

    if (result.rows.length === 0) {
      return null;
    }

    // rows[0] === data[0] in Python
    return result.rows[0];

  } catch (err) {
    console.error("Error finding app:", err);
    throw err;
  } finally {
    client.release();
  }
}


export async function downloadApp(appId) {
  const app = await findApp(appId);

  if (!app) {
    throw new Error("App not found");
  }
  console.log(app);

  const appUrl = app.app_url

  // console.log(appUrl);

  const download_url = await getFinalDownloadLink(appUrl);
  return download_url
}


// downloadApp(228)

const main = async () => {

  // STEP 1
  // const url = "https://en.uptodown.com/android/apps/latest-updates"
  // const apps = await fetchUptoDownApi(url)

  // apps.map(async (app, index) => {
  //   console.log(index);

  //   const app_obj = {
  //   app_id: app.appID,
  //   name: app.name,
  //   platform_id: app.platformID,
  //   short_description: app.shortDescription,
  //   promoted_app: app.promotedApp,
  //   author: app.author,
  //   platform_url: app.platformURL,
  //   platform_name: app.platformName,
  //   icon_url: app.iconURL,
  //   app_url: app.appURL
  // }; 
  // const { sql, values } = buildSqlQuery("apps", app_obj);
  // const response_db = await pool.query(sql, values)
  // console.log('inserted app in list of apps');
  // console.log(response_db.rows)
  // console.log(response_db.rows);







  // })



  // STEP 2
  // const apps = await fetchApps("apps")
  const apps = []
  apps.map(async (app) => {

    const app_info = await scrapeUptodown(app.app_url)
    const { appSql } = buildAppSql(app.id, app_info);
    // console.log(appSql)
    const response_db_app = await pool.query(appSql)
    console.log(response_db_app.rows[0].id);

    const { screenshotsSql, versionsSql } = buildAppSql(response_db_app.rows[0].id, app_info);

    const response_db_ss = await pool.query(screenshotsSql)
    console.log(response_db_ss.rows);

    const response_db_v = await pool.query(versionsSql)
    console.log(response_db_v);

    // STEP 3
    // const download_Url = await getFinalDownloadLink(appURL)
    // request.downlaod(download_Url)

    // STEP 4
    // insert_to_database(table, query)
  })

}

// main();