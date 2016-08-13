let service = "http://127.0.0.1:8000/reddit";
let titles = document.querySelectorAll("a.title.srTagged"); // Visible posts seem to have srTagged class
let internalPost = /https?:\/\/(www|np)\.reddit\.com\/r\//;

titles.forEach(function (t) {
  if (internalPost.exec(t.href) !== null) {
    return; // Reddit doesn't support searching for subreddits with self posts (very well)
  }
  console.log("Searching "+ t.href);

  $.get(service, { url: t.href } )
  .done(function( data ) {
    let subreddits = JSON.parse(data)
    subreddits.forEach(function(subreddit) {
      var newElement = document.createElement("a");
      newElement.style.color = "red";
      newElement.classList = ["subreddit", "hover"];
      newElement.textContent = "(" + subreddit + ") ";
      newElement.href = "https://www.reddit.com" + subreddit;
      var parent = t.parentElement;
      parent.appendChild(newElement);
    });
  });
});
