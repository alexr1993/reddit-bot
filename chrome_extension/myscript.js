let service =  "http://localhost:8080/search";// "https://jukeboxxy.com/reddit";
let internalPost = /https?:\/\/((www|np)\.)?reddit\.com\/r\//;

var fetchedPosts = {};

// TODO images hosted on i.reddit will not be linked from the <a>.
// The post links to the comments, but the thumbnail/expando loads the image both on reddit and RES

var presentSubmissionData = function(linkTag, subData) {
  let parentElement  = linkTag.parentElement.parentElement;
  if (!Array.from(parentElement.classList).includes("entry")) {
    console.log("Cannot find submission top-level container for post " + linkTag.href);
  }
  console.log(parentElement);

  subData.sort(function(a, b) {
    let keyA = a.created_utc, keyB = b.created_utc;
    if (keyA > keyB) {
      return -1;
    }
    return 1;
  });

  let list = document.createElement("ul");
  parentElement.appendChild(list);
  subData.forEach(function(subDatum) {
    let subreddit = subDatum.subredditName;
    var newElement = document.createElement("a");

    let date = new Date(subDatum.created_utc * 1000);

    newElement.style.color = "red";
    newElement.classList = ["subreddit", "hover"];
    newElement.textContent = date.toUTCString() + " " + subreddit + " " + subDatum.score;
    newElement.href = "https://www.reddit.com/r/" + subreddit;
    let item = document.createElement("li");
    item.appendChild(newElement);
    list.appendChild(item);
  });
}

var fetchSubreddits = function() {
  // Users with RES will have some invisible posts, only those with srTagged class are visible
  var posts = document.querySelectorAll("a.title.srTagged");
  if (posts.length === 0) {
    posts = document.querySelectorAll("a.title");
  }
  var unfetchedPosts = [];
  var unfetchedUrls = [];

  posts.forEach(function (p) {
    let url = p.href;
    if (fetchedPosts[url] === undefined && internalPost.exec(url) === null) {
      unfetchedPosts.push(p);
      unfetchedUrls.push(p.href);
    }
  });

  if (unfetchedPosts.length === 0) {
    return;
  }

  console.log("unfetchedPosts" + unfetchedUrls.length);

  $.ajax({
    type: "POST",
    url: service,
    contentType: "application/json",
    data: JSON.stringify({urls: unfetchedUrls}),
    dataType: "json",
    success: function( submissionData ) {
      unfetchedPosts.forEach(function(p) {
        let subData = submissionData.submissions[p.href];
        if (subData === undefined) {
          return; // Data is not available yet
        }

        // TODO register fetched post
        fetchedPosts[p] = true;

        presentSubmissionData(p, subData);
      });
    }
  });
};

setInterval(fetchSubreddits, 1000);
