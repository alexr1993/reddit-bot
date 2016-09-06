console.log("Subreddit finder running");

let service = "https://jukeboxxy.com/search"; //"http://localhost:8080/search";//;
let internalPost = /https?:\/\/((www|np)\.)?reddit\.com\/r\//;
let MAX_ROWS = 5;
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
  if (pageTabs == null) {
    return;
  }
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

let formatDate = function(date) {
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

let formatTitle = function(title) {
  if (title === undefined || title === null) {
    return "";
  }

  return title;
}

let compareTo = function(numA, numB) {
  if (numA < numB) return -1;
  if (numB < numA) return 1;
  return 0;
}

let createToggleButton = function(table, tableHeading) {
  let toggleButton = document.createElement("span");
  toggleButton.style.cursor = "pointer";
  table.style.display = showingAll ? "block" : "none";
  table.classList = ["greentable"];

  toggleButton.textContent = tableHeading;
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
  return toggleButton;
};

let createRowToggleButton = function(hideableRows) {
  let button = document.createElement("span");
  let visible = false;

  button.textContent = "(show more)"
  button.style.cursor = "pointer";
  button.style.paddingLeft = "3px";
  button.onclick = function(e) {
    if (visible) {
      hideableRows.forEach(function(r) { r.style.display = "none"});
      visible = false;
      button.textContent = "(show more)"
    } else {
      hideableRows.forEach(function(r) { r.style.display = "table-row"});      
      button.textContent = "(show less)";
      visible = true;
    }
  }

  return button;
};

let presentSubmissionData = function(parentElement, subData, tableHeading) {
  let hiddenRows = {};
  if (subData.length > MAX_ROWS) {
    subData.sort(function(a, b) { return compareTo(a.score, b.score); });
    let defaultHidden = subData.slice(0, subData.length - MAX_ROWS);
    defaultHidden.forEach(function(dH) { hiddenRows[dH.createdUtc] = true; });
  }

  subData.sort(function(a, b) { return compareTo(a.createdUtc, b.createdUtc); }).reverse();
  let table = document.createElement("table");
  table.style.marginTop = "3px";
  let toggleButton = createToggleButton(table, tableHeading);
  let hideableRows = [];

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
      cell.noWrap = true;
      return cell;
    }

    let row = document.createElement("tr");
    row.appendChild(td(dateCell));
    row.appendChild(td(subredditCell));
    row.appendChild(td(scoreCell));

    if (hiddenRows[subDatum.createdUtc]) {
      hideableRows.push(row);
      row.style.display = "none";
    }
    table.appendChild(row);
  });

  parentElement.appendChild(toggleButton);

  if (subData.length > MAX_ROWS) {
    toggleButton.onclick = undefined;
    toggleButton.style.cursor = "default";
    let rowToggleButton = createRowToggleButton(hideableRows);
    parentElement.appendChild(rowToggleButton);
  }
  parentElement.appendChild(table);

}

let fetchSubreddits = function() {
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

        if (subData.length < 2) {
          subData = [];
        }
        presentSubmissionData(p.parentElement.parentElement, subData, Math.max(0, subData.length - 1) + " other submissions");
      });
      isRequestInFlight = false;
    },
    error: function(xhr, error) {
      isRequestInFlight = false;
    }
  });
};

var pageUrlFetched = null;
var fetchingPageUrl = false;

let fetchPageUrl = function() {
  let url = window.location.href;

  $.ajax({
    type: "POST",
    url: service,
    contentType: "application/json",
    data: JSON.stringify({urls: [url]}),
    dataType: "json",
    success: function( submissionData ) {
      let subData = submissionData.submissions[url];
      if (subData === undefined) {
        fetchingPageUrl = false;
        return; // Data is not available yet
      }

      presentSubmissionData(document.getElementById("watch-headline-title"), subData, subData.length + " submissions on Reddit");
      pageUrlFetched = window.location.href;
      fetchingPageUrl = false;
    },
    error: function(xhr, error) {
      fetchingPageUrl = false;
    }
  });
}

// Never stop checking because never-ending reddit might be on
let runRequest = function() {
  // TODO check we are on Reddit
  if (!isRequestInFlight) {
    isRequestInFlight = true;
    fetchSubreddits();
  }
  setTimeout(runRequest, 1000);
};

runRequest();

// Never stop checking because youtube doesn't load new pages when you follow a link to another video
let runPageUrlRequest = function() {
  // TODO check we are on a youtube video page
  if (fetchingPageUrl) {
    setTimeout(runPageUrlRequest, 1000);
    return;
  }
  
  if (pageUrlFetched === window.location.href) {
    setTimeout(runPageUrlRequest, 1000);
    return;
  }

  fetchingPageUrl = true;
  fetchPageUrl();      

  setTimeout(runPageUrlRequest, 1000);
};
