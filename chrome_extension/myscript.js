let service = "https://jukeboxxy.com/reddit";
let internalPost = /https?:\/\/((www|np)\.)?reddit\.com\/r\//;

var fetchedPosts = [];

var fetchSubreddits = function() {
  var posts = document.querySelectorAll("a.title.srTagged"); // Visible posts seem to have srTagged class
  if (posts.length <= fetchedPosts.length) {
    return;
  }

  let startIx = fetchedPosts.length;
  fetchedPosts = posts;

  var newPosts = [];
  if (startIx === 0) {
    newPosts = posts;
  } else {
    newPosts = Array.from(posts).slice(startIx - 1);
  }

  console.log("newPosts" + newPosts.length);

  newPosts.forEach(function (t) {
    if (internalPost.exec(t.href) !== null) {
      return; // Reddit doesn't support searching for subreddits with self posts (very well)
    }
    console.log("Searching "+ t.href);

    // TODO make this work with never ending reddit
    $.get(service, { url: t.href } )
    .done(function( data ) {
      let subreddits = JSON.parse(data)
      subreddits.forEach(function(subreddit) {
        var newElement = document.createElement("a");
        newElement.style.color = "red";
        newElement.classList = ["subreddit", "hover"];
        newElement.textContent = " " + subreddit;
        newElement.href = "https://www.reddit.com" + subreddit;
        var parent = t.parentElement;
        parent.appendChild(newElement);
      });
    });
  });
};

setInterval(fetchSubreddits, 1000);
