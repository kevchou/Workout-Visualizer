var w = 600;
var h = 400;
var padding = 30;

var svg = d3.select("body").append("svg")
    .attr("height", h)
    .attr("width", w);

var x = d3.scaleTime()
    .range([padding, w - padding * 2]);

var y = d3.scaleLinear()
    .range([h - padding, padding]);

var parseTime = d3.timeParse("%Y-%m-%d");


function parseData(data) {
    data.forEach(function (d) {
        d.date = parseTime(d.date);
        d.weight = +d.weight;
    });
    return data;
}

// Add line for the weight 
var weightpath = svg.append("path")
    .attr("id", "weightpath");


var path = d3.line()
    .x(function (d) { return x(d.date); })
    .y(function (d) { return y(d.weight); });

// Add the X Axis
var xaxis = svg.append("g")
    .attr("class", "axis");

// Add the Y Axis
var yaxis = svg.append("g")
    .attr("class", "axis")

x.domain([d3.timeParse("%Y-%m-%d")("2016-01-01"), d3.timeParse("%Y-%m-%d")("2017-12-31")]);
y.domain([0, 100]);

xaxis.attr("transform", "translate(0," + (h - padding) + ")")
    .call(d3.axisBottom(x));

yaxis.attr("transform", "translate(" + padding + ",0)")
    .call(d3.axisLeft(y));



d3.selectAll(".myCheckbox").on("change", update);
update();

function update() {

  var choices = [];

  d3.selectAll(".myCheckbox").each(function (d) {
    
    cb = d3.select(this);

    if (cb.property("checked")) {
      choices.push(cb.property("value"));
    }
  });

  d3.selectAll(".line").remove();
  if (choices.length > 0) {
      drawGraph(choices);
  }
}

function drawGraph(choices) {
  
  d3.json('/data/multi/' + choices, function (error, data) {
    if (error) throw error;

    data = parseData(data);
    x.domain(d3.extent(data, function (d) { return d.date; }));
    y.domain([0, d3.max(data, function (d) { return d.weight; }) * 1.05]);

    xaxis.call(d3.axisBottom(x));
    yaxis.call(d3.axisLeft(y));

    // Nest the entries by symbol
    var dataNest = d3.nest()
        .key(function(d) { return d.exercise; })
        .entries(data);

    // set the colour scale
    var color = d3.scaleOrdinal(d3.schemeCategory10);

    // Loop through each symbol / key
    dataNest.forEach(function(d,i) { 
                svg.append("path")
                    .attr("class", "line")
                    .style("stroke", function() { // Add the colours dynamically
                        return d.color = color(d.key); })
                    .attr("d", path(d.values));        
            });
  });

}
// d3.selectAll(".myCheckbox").on("change", update);
// update();


// function update() {

//     var choices = [];

//     d3.selectAll(".myCheckbox").each(function (d) {

//         cb = d3.select(this);

//         if (cb.property("checked")) {
//             choices.push(cb.property("value"));
//         }
//     });

//     drawGraph(choices);
// }

// function drawGraph(choices) {

//     d3.json('/data/multi/' + choices, function (error, data) {
//         if (error) throw error;
//     });

//}