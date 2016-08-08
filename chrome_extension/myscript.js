let titles = document.querySelectorAll("a.title");
titles.forEach(function (t) { console.log( t.href) });
titles.forEach(function (t) {
  var newElement = document.createElement("b");
  newElement.textContent = "(blah) ";
  var parent = t.parentElement;
  parent.insertBefore(newElement, t);
});
