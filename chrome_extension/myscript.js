let titles = document.querySelectorAll("a.title");
titles.forEach(function (t) { console.log( t.href) });
titles.forEach(function (t) {
  $.get( "http://127.0.0.1:5000/", { url: t.href } )
  .done(function( data ) {
    let subreddits = JSON.parse(data)
    subreddits.forEach(function(subreddit) {
      var newElement = document.createElement("a");
      newElement.style.color = "red";
      newElement.classList = ["subreddit", "hover"];
      newElement.textContent = "(" + subreddit + ") ";
      newElement.href = "https://www.reddit.com" + subreddit;
      var parent = t.parentElement;
      parent.insertBefore(newElement, t);
    });
  });

});
