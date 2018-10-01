// Get a reference to the table body
var tbody = d3.select("tbody");

// console.log(data);

// Assign the data from `data.js` to a descriptive variable
var filtered;
var filteredData;

// Refactor to use Arrow Functions!
data.forEach((appendTable) => {
    var row = tbody.append("tr");
    Object.entries(appendTable).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
});
 
// Select the submit button
var submit = d3.select("#filter-btn");

// Use D3 `.on` to attach a click handler
submit.on("click", function() {
  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  var inputElement = d3.select("#datetime");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");
  console.log(inputValue);

  filteredData = data.filter(data => data.datetime === inputValue);

  var tbody = d3.select("tbody");
  tbody.html('');
  filteredData.forEach((appendTable) => {
    var row = tbody.append("tr");
    Object.entries(appendTable).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
  });
});