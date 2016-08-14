let service =  "http://localhost:8080/search";// "https://jukeboxxy.com/reddit";
let internalPost = /https?:\/\/((www|np)\.)?reddit\.com\/r\//;

var fetchedPosts = {};

var fetchSubreddits = function() {
  var posts = document.querySelectorAll("a.title.srTagged"); // Visible posts seem to have srTagged class
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

        subData.forEach(function(subDatum) {
          let subreddit = subDatum.subredditName;
          var newElement = document.createElement("a");
          newElement.style.color = "red";
          newElement.classList = ["subreddit", "hover"];
          newElement.textContent = " " + subreddit;
          newElement.href = "https://www.reddit.com" + subreddit;
          var parent = p.parentElement;
          parent.appendChild(newElement);
        });
      });
    }
  });
};

setInterval(fetchSubreddits, 1000);
