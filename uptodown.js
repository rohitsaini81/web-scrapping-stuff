
const axios = require("axios");
const cheerio = require("cheerio");

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

    console.log("Download page:", downloadPageUrl);

    // STEP 3 — Load the download page and extract token
    const downloadPage = await axios.get(downloadPageUrl);
    const $$ = cheerio.load(downloadPage.data);

    const token = $$("#detail-download-button").data("url");

    if (!token) {
      throw new Error("Download token not found.");
    }

    console.log("Token:", token);

    // Build the redirect URL exactly like the browser iframe does
    const iframeUrl = "https://dw.uptodown.net/dwn/" + token;

    console.log("Redirect URL:", iframeUrl);

    // STEP 4 — Follow redirects to get the FINAL download link
    const final = await axios.get(iframeUrl, {
      maxRedirects: 10,
      validateStatus: () => true, // allow redirects
    });

    const finalUrl = final.request.res.responseUrl;

    console.log("\n🔥 FINAL DIRECT DOWNLOAD LINK:");
    console.log(finalUrl);

  } catch (err) {
    console.error("Error:", err.message);
  }
}

// getFinalDownloadLink("https://tiktok-lite.en.uptodown.com/android");




// document.getElementsByClassName("content")[1].childNodes[1]
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

// scrapeUptodown("https://pixelc.en.uptodown.com/android").then((d)=>console.log(d))

/*
 step 0 it's all ssr : https://en.uptodown.com/
 listed all apps of uptodown
 step 1 select any random app
https://tiktok-lite.en.uptodown.com/android

step 2 get that download page url form ancor tag inside get latest version download button
https://tiktok.en.uptodown.com/android/download

step 3 extract download token and fetch download link using this function :*/
// (function() {
//   const token = document.querySelector('#detail-download-button').dataset.url;
//   const url = "https://dw.uptodown.net/dwn/" + token;

//   const iframe = document.createElement("iframe");
//   iframe.style.display = "none";

//   iframe.onload = function () {
//     console.log("Final URL:", iframe.src);
//     document.body.removeChild(iframe);
//   };

//   iframe.src = url;
//   document.body.appendChild(iframe);
// })();

