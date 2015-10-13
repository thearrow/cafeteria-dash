///<reference path="external/d3.min.js"/>
///<reference path="external/metricgraphics.min.js"/>


var today = new Date();
var yesterday = subtractDays(today, 1);

if(!window.chrome){
	alert('This page is best viewed in Google Chrome. \nIf you continue, the graphs might not display.');
}
getMenu();
getCurrentInfo();
getWeather();
graphForDate(today, "#today");
graphForDate(yesterday, "#yesterday");


function getMenu() {
	var menuOrder = ["Entrée", "Chef's Special", "Grill Special", "Grill", "Soup", "Dessert"];

	d3.json("/menu", function (data)
	{
		var menuArray = [];
		for (var category in data){
			menuArray.push({category: category, items: data[category]});
		}
		menuArray.sort(function(x,y) {
			if(menuOrder.indexOf(x.category) < menuOrder.indexOf(y.category))
				return -1;
			else if(menuOrder.indexOf(x.category) > menuOrder.indexOf(y.category))
				return 1;
			else return 0;
		});

		var menu = d3.select(".menu").append("ul");
		menuDivs = menu.selectAll("li.category")
			.data(menuArray);
		var enter = menuDivs.enter().append("li")
			.classed("category", true)
			.text(function(d){ return d.category; });

		var items = enter.append("ul")
			.classed("items", true)
			.selectAll("li.item")
				.data(function(d){ return d.items; });
		items.enter().append("li")
			.classed("item", true)
			.text(function(d){ return d[0]; });

		d3.select(".menu").append("p")
			.classed("culinary-link", true)
			.append("a")
				.attr("href", "http://teamportal/sites/admin/Culinary/Lists/Menu%20Items/Simplified.aspx")
				.attr("target", "_blank")
				.text("Culinary Site");
	});
}


function getCurrentInfo()
{
	if (isBeforeTenThirty(today))
	{
		d3.select("#today").append('p')
			.text("Data will start displaying at 10:30am!");
	}

	d3.json('/current', function (data)
	{
		var crowding = data.currentNum.toFixed(2);
		d3.select("#current-num")
			.text(crowding + " / 10")
			.style("color", function() {
				if(crowding < 5)
					return 'green';
				else if(crowding >= 5 && crowding <= 7)
					return 'orange';
				else
					return 'red';
			});
		d3.select("#current-img").attr("src", data.currentImg);
	});
}


function getWeather()
{
	//only fetch weather when cass is open
	// if (isBeforeTenThirty(today) || isAfterTwo(today))
	// {
	// 	d3.selectAll(".right img").remove();
	// 	d3.select(".right").append('p')
	// 		.text('Weather will be shown between 10:30am - 2:00pm!');
	// 	return;
	// }

	d3.json('/weather', function (data){
		var weather = data.current_observation;
		d3.select("#weather-description").text(weather.weather);
		d3.select("#weather-icon")
			.attr("src", weather.icon_url)
			.attr("title", weather.icon);

		d3.select("#weather-temperature").text(weather.temp_f + " F");
		drawThemometer(d3.select("#weather-thermometer"), weather.temp_f);

		d3.select("#weather-wind-speed").text("Wind: " + weather.wind_mph + " MPH");
		d3.select("#weather-wind-gust").text("Gusts: " + weather.wind_gust_mph + " MPH");
		d3.select("#weather-uv").text("UV: " + weather.UV + " / 12");
		d3.select("#weather-humidity").text("Humidity: " + weather.relative_humidity);

		d3.select("#weather-updated").text(weather.observation_time);
		d3.select("#weather-attribution")
			.attr("src", weather.image.url)
			.attr("title", weather.image.title);
		d3.select("#weather-link").attr("href", weather.ob_url);
	});
}


function graphForDate(date, id)
{
	var request = "/date/" + d3.time.format("%m-%d-%Y")(date);
	d3.json(request, function (data)
	{
		if (data.data[0].length === 0) return;

		for (var i = 0; i < data.data[1].length; i++)
		{
			if(data.data[0].length > i){
				data.data[0][i].time = convertDateToUTC(new Date(data.data[0][i].time));
			}
			data.data[1][i].time = convertDateToUTC(new Date(data.data[1][i].time));
		}

		var start = convertDateToUTC(new Date(date.setUTCHours(10, 30, 0, 0)));
		var open = convertDateToUTC(new Date(date.setUTCHours(11, 0, 0, 0)));
		var close = convertDateToUTC(new Date(date.setUTCHours(13, 59, 0, 0)));
		var end = convertDateToUTC(new Date(date.setUTCHours(14, 0, 0, 0)));

		var markers = [
			{ 'time': open, 'label': 'Open' },
			{ 'time': close, 'label': 'Close' }
		];

		MG.data_graphic({
			title: '',
			data: data.data,
			target: id,
			x_accessor: 'time',
			y_accessor: 'data',
			min_x: start,
			min_y: 1.0,
			max_x: end,
			max_y: 10.0,
			full_width: true,
			height: 300,
			markers: markers,
			point_size: 4,
			show_tooltips: false,
			legend: ['Current', "Average"],
			legend_target: id+'-legend',
		});

		//custom legend average text
		d3.select(id + '-legend .mg-line2-legend-color').text("- - - " + data.days + "-Day Average");

		//custom area for multiline charts
		var area = d3.select(id + ' .mg-line1-color').node().cloneNode(true);
		d3.select(area)
			.attr('class', 'mg-main-area mg-area1-color')
			.attr('d', function () { return d3.select(area).attr('d') + 'V500H50Z'; });
		d3.select(id + ' svg').node().insertBefore(area, d3.select(id + ' .mg-voronoi').node());

		buildGradient(id);
	});
}


function buildGradient(id)
{
	d3.select(id + " defs").append("linearGradient")
		  .attr("id", "gradient")
		  .attr("gradientUnits", "userSpaceOnUse")
		  .attr("x1", 0).attr("y1", 188)
		  .attr("x2", 0).attr("y2", 138)
		.selectAll("stop")
		  .data([
			{ offset: "0%", color: "green" },
			{ offset: "50%", color: "yellow" },
			{ offset: "100%", color: "red" }
		  ])
		.enter().append("stop")
		  .attr("offset", function (d) { return d.offset; })
		  .attr("stop-color", function (d) { return d.color; });
}


function drawThemometer(div, temp) {
	var height = 80;
	var width = 50;
	var innerwidth = 15;

	var svg = div.append('svg')
		.classed('thermometer', true)
		.attr('width', width)
		.attr('height', height)
		.style('margin', 'auto')
		.style('position', 'relative')
		.style('margin-top', '10px');

	var y = d3.scale.linear()
		.domain([30, 100])
		.range([height, 10]);
	var yAxis = d3.svg.axis().scale(y).ticks(3).orient("left");

	svg.append('g')
		.attr('transform', 'translate('+innerwidth*2+',0)')
		.call(yAxis);

	var rect = svg.append('rect')
		.attr('width', innerwidth)
		.attr('y', y(temp))
		.attr('x', innerwidth*2)
		.attr('height', height-y(temp))
		.style('fill', function(d) {
			if(temp <= 60) return 'blue';
			else if(temp > 60 && temp < 80) return 'green';
			else if(temp >= 80 && temp < 90) return 'orange';
			else if(temp >= 90) return 'red';
		});
}


function convertDateToUTC(date)
{
	return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
}


function subtractDays(date, days)
{
	result = new Date();
	return new Date(result.setDate(date.getDate() - days));
}


function isBeforeTenThirty(date) {
	return (date.getHours() < 10 || (date.getHours() === 10 && date.getMinutes() < 30));
}


function isAfterTwo(date) {
	return (date.getHours() > 14 || (date.getHours() === 14 && date.getMinutes() > 0));
}