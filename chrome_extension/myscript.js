let service = "https://jukeboxxy.com/search";// 
let internalPost = /https?:\/\/((www|np)\.)?reddit\.com\/r\//;

var fetchedPosts = {};
let fontColor = "rgb(0, 204, 102)";
var isRequestInFlight = false;
var showingAll = true;
/* Add button to toggle table on page */
(function() {
  var toggle = function() {
    showingAll = !showingAll;
    pageToggle.textContent = showingAll ? "Hide Post Lists" : "Show Post Lists";

    let tables = document.querySelectorAll(".greentable");
    for (var i = 0; i < tables.length; i++) {
      tables[i].style.display = showingAll ? "block" : "none";
    }
  }

  let pageToggle = document.createElement("a");
  pageToggle.style.cursor = "pointer";
  let li = document.createElement("li");
  li.appendChild(pageToggle);
  pageToggle.onclick = toggle;
  pageToggle.textContent = showingAll ? "Hide Post Lists" : "Show Post Lists";
  let pageTabs = document.querySelector(".tabmenu");
  pageTabs.appendChild(li);
}());

let getDateString = function(date) {
  let options = {
      weekday: "long", year: "numeric", month: "short",
      day: "numeric", hour: "2-digit", minute: "2-digit"
  };
  return date.toLocaleTimeString("en-us", options);
};


// TODO images hosted on i.reddit will not be linked from the <a>.
// The post links to the comments, but the thumbnail/expando loads the image both on reddit and RES

var createCell = function() {
  let cell = document.createElement("a");
  cell.style.color = fontColor;
  return cell;
};

var formatDate = function(date) {
  let now = new Date(Date.now());

  let diffSecs = (now.getTime() - date.getTime()) / 1000;
  if (diffSecs < 60) {
    return Math.floor(diffSecs) + " seconds ago";
  }

  let diffMins = diffSecs/60;
  if (diffMins < 60) {
    return Math.floor(diffMins) + " minutes ago";
  }

  let diffHours = diffMins/60;
  if (diffHours < 24) {
    return Math.floor(diffHours) + " hours ago";
  }

  let diffDays = diffHours/24;
  if (diffDays < 31) {
    return Math.floor(diffDays) + " days ago";
  }

  let diffMonths = diffDays/30;
  if (diffMonths < 12) {
    return Math.floor(diffMonths) + " months ago";
  }

  return getDateString(date);
  //let diffYears = diffMonths/12;
  //return Math.floor(diffYears) + " years ago";
};

var presentSubmissionData = function(linkTag, subData) {
  let parentElement = linkTag.parentElement.parentElement;
  if (!Array.from(parentElement.classList).includes("entry")) {
    console.log("Cannot find submission top-level container for post " + linkTag.href);
  }

  subData.sort(function(a, b) {
    let keyA = a.createdUtc, keyB = b.createdUtc;
    if (keyA > keyB) {
      return -1;
    }
    return 1;
  });
  let toggleButton = document.createElement("div");
  toggleButton.style.cursor = "pointer";
  let table = document.createElement("table");
  table.style.display = showingAll ? "block" : "none";
  table.classList = ["greentable"];
  toggleButton.textContent = subData.length - 1 + " other submissions";
  toggleButton.color = fontColor;
  toggleButton.style.paddingTop = "3px";
  toggleButton.style.paddingBottom = "4px";

  toggleButton.onclick = function (e) {
    if (table.style.display === "block") {
      table.style.display = "none";
    } else {
      table.style.display = "block";
    }
  };

  parentElement.appendChild(toggleButton);

  parentElement.appendChild(table);
  subData.forEach(function(subDatum) {
    let subreddit = subDatum.subredditName;
    let dateCell = createCell();
    let subredditCell = createCell();
    let scoreCell = createCell();

    let date = new Date(subDatum.createdUtc * 1000);
    dateCell.textContent = formatDate(date);
    dateCell.href = subDatum.permalink;

    subredditCell.textContent = "/r/" + subreddit;
    subredditCell.href = "https://www.reddit.com/r/" + subreddit;

    scoreCell.textContent = subDatum.score;

    let td = function(element) {
      let cell = document.createElement("td");
      cell.appendChild(element);
      cell.style.paddingRight = "10px";
      return cell;
    }

    let row = document.createElement("tr");
    row.appendChild(td(dateCell));
    row.appendChild(td(subredditCell));
    row.appendChild(td(scoreCell));
    table.appendChild(row);
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
    isRequestInFlight = false;
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

        fetchedPosts[p] = true;
        presentSubmissionData(p, subData);
      });
      isRequestInFlight = false;
    }
  });
};

// Never stop checking because never-ending reddit might be on
let runRequest = function() {
  if (!isRequestInFlight) {
    isRequestInFlight = true;
    fetchSubreddits();
  }
  setTimeout(runRequest, 1000);
};

runRequest();
