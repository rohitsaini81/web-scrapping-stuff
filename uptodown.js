
const axios = require("axios");
const cheerio = require("cheerio");
const FormData = require('form-data');



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
    return finalUrl;
    // console.log("\n🔥 FINAL DIRECT DOWNLOAD LINK:");
    // console.log(finalUrl);

  } catch (err) {
    console.error("Error:", err.message);
  }
}
// getFinalDownloadLink("https://tiktok-lite.en.uptodown.com/android");.apk url




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








const main = async () => {

  // STEP 1
  const url = "https://en.uptodown.com/android/apps/latest-updates"
  // const apps = await fetchUptoDownApi(url)
  const apps = []
  
  apps.map(async (app,index) => {
    console.log(index);
    
    const app_obj = {
      appID: app.appID,
      name: app.name,
      platformID: app.platformID,
      shortDescription: app.shortDescription,
      promotedApp: app.promotedApp,
      author: app.author,
      platformURL: app.platformURL,
      platformName: app.platformName,
      iconURL: app.iconURL,
      appURL: app.appURL
    }
    // const { sql, values } = buildSqlQuery("Apps", app_obj);



    // STEP 2
    // const app_info = await scrapeUptodown(app.appURL)
    // const { appSql, screenshotsSql, versionsSql } = buildAppSql(app_info);

    // STEP 3
    // const download_Url = await getFinalDownloadLink(appURL)
    // request.downlaod(download_Url)




    // STEP 4
    // insert_to_database(table, query)

  })


}

// main();



function buildSqlQuery(table, data) {
  const columns = Object.keys(data);
  const placeholders = columns.map(() => "?");
  const values = Object.values(data);

  const sql = `
    INSERT INTO ${table} (${columns.join(", ")})
    VALUES (${placeholders.join(", ")});
  `;

  return { sql, values };
}

function buildAppSql(app_info) {
  // Escape single quotes for SQL safety
  const esc = (v) =>
    typeof v === "string" ? v.replace(/'/g, "''") : v;

  // --- MAIN APP INSERT ---------------------------------

  const appSql = `
INSERT INTO apps (
  name, version, author, rating, reviews, downloads, last_updated,
  description, package_name, category, requirements
) VALUES (
  '${esc(app_info.name)}',
  '${esc(app_info.version)}',
  '${esc(app_info.author)}',
  ${Number(app_info.rating)},
  ${Number(app_info.reviews)},
  ${Number(app_info.downloads)},
  '${new Date(app_info.lastUpdated).toISOString().split("T")[0]}',
  '${esc(app_info.description)}',
  '${esc(app_info.packageName)}',
  '${esc(app_info.category)}',
  ARRAY[${app_info.requirements.map(r => `'${esc(r)}'`).join(", ")}]
)
RETURNING id;`.trim();


  // --- SCREENSHOTS INSERT -------------------------------

  const screenshotsSql = app_info.screenshots.map(url => `
INSERT INTO app_screenshots (app_id, url)
VALUES ($APP_ID$, '${esc(url)}');`.trim()
  ).join("\n");


  // --- OLDER VERSIONS INSERT ----------------------------

  const versionsSql = app_info.olderVersions.map(v => `
INSERT INTO app_versions (app_id, type, version, sdk, release_date, url, version_id)
VALUES (
  $APP_ID$,
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
