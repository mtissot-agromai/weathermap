// Leaflet map setup
const map = L.map('map').setView([-14, -50], 5);

L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles © Esri',
    maxZoom: 19
}).addTo(map);

L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Labels © Esri',
    maxZoom: 19,
    opacity: 1.0
}).addTo(map);

let marker = L.marker([document.getElementById('latitude').value, document.getElementById('longitude').value]).addTo(map);

map.on('click', function (e) {
    document.getElementById('latitude').value = e.latlng.lat.toFixed(4);
    document.getElementById('longitude').value = e.latlng.lng.toFixed(4);
    marker.setLatLng(e.latlng).bindPopup(`(${e.latlng.lat.toFixed(4)}, ${e.latlng.lng.toFixed(4)})`);
});

document.getElementById('weather-form').addEventListener('change', function () {
    const lat = parseFloat(document.getElementById('latitude').value);
    const lng = parseFloat(document.getElementById('longitude').value);
    marker.setLatLng([lat, lng]);
});

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}

document.getElementById('variable-selector').addEventListener('change', function () {
    const variable = this.value;
    var max = {
        x: weatherData.dates,
        y: weatherData[variable]['max'],
        type: 'scatter',
        name: variable.charAt(0).toUpperCase() + variable.slice(1) + ' Max',
        line: {dash: 'dot', width: 1, color: colors_variable[variable]['max']},
        hovertamplate: ''
    };
    var min = {
        x: weatherData.dates,
        y: weatherData[variable]['min'],
        type: 'scatter',
        name: variable.charAt(0).toUpperCase() + variable.slice(1) + ' Min',
        line: {dash: 'dot', width: 1, color: colors_variable[variable]['min']},
        hovertamplate: ''
    };
    var avg = {
        x: weatherData.dates,
        y: weatherData[variable]['avg'],
        type: 'scatter',
        name: variable.charAt(0).toUpperCase() + variable.slice(1) + ' Avg',
        line: {color: colors_variable[variable]['avg']},
        hovertamplate: ''
    };
    Plotly.react('other-graph', [max, avg, min], { title: names_from_variable[variable], hovermode: 'x unified' });
});

let safra_dict = {
    '2425': ['2024-08-20', '2025-06-20'],
    '2324': ['2023-08-20', '2024-06-20'],
    '2223': ['2022-08-20', '2023-06-20'],
    '2122': ['2021-08-20', '2022-06-20'],
    '2021': ['2020-08-20', '2021-06-20'],
    '1920': ['2019-08-20', '2020-06-20']
};

document.getElementById('safra').addEventListener('change', function () {
    const safra = this.value;
    if (safra!='noSafra'){
    document.getElementById('start_date').value = safra_dict[safra][0];
    document.getElementById('end_date').value   = safra_dict[safra][1];
    }
});

document.getElementById('start_date').addEventListener('change', function () {
    const startDate = this.value;
    const endDate = document.getElementById('end_date').value;
    const startDate_date = new Date(startDate);
    const endDate_date = new Date(endDate);
    if (startDate > endDate) {
        document.getElementById('end_date').value = this.value;
    }

    const safra = document.getElementById('safra').value;
    if (startDate != safra_dict[safra][0]) {
        document.getElementById('safra').value = 'noSafra';
    }
});

document.getElementById('end_date').addEventListener('change', function () {
    const endDate = this.value;
    const startDate = document.getElementById('start_date').value;
    const endDate_date = new Date(endDate);
    const startDate_date = new Date(startDate);
    if (endDate < startDate) {
        document.getElementById('start_date').value = this.value;
    }

    const safra = document.getElementById('safra').value;
    if (endDate != safra_dict[safra][1]) {
        document.getElementById('safra').value = 'noSafra';
    }
});

let weatherData = {};

const names_from_variable = {
    'temp': 'Temperature',
    'rhum': 'Relative Humidity',
    'wspd': 'Wind Speed',
}

const colors_variable = {
    temp: {max: 'rgba(226, 80, 43, 0.8)', min: 'rgba(0, 115, 195, 0.5)', avg: 'rgb(0, 0, 0)'},
    rhum: {max: 'rgba(0, 120, 100, 1)', min: 'rgba(255, 180, 0, 0.8)', avg: 'rgba(0, 200, 150, 0.85)'},
    wspd: {max: 'rgba(0, 60, 130, 1)', min: 'rgba(0, 200, 255, 0.8)', avg: 'rgba(0, 140, 255, 0.85)'},
};

// document.getElementById('show_alerts').addEventListener('change', function(e){
//     console.log(this.checked);
//     if (this.checked){
//         Plotly.react('prcp-graph', [{
//             x: weatherData.dates,
//             y: weatherData.precipitation,
//             type: 'bar',
//             name: 'precipitation',
//             marker: {color: weatherData.colors_prcp},
//             customdata: weatherData.prcp_cumulative,
//             hovertemplate: 'Date: %{x}<br>Precipitation: %{y} mm<br>Cumulative: %{customdata:.1f}<extra></extra>',
//         }], { title: 'Precipitation', hovermode: 'x unified' });
//     } else {
//         Plotly.react('prcp-graph', [{
//             x: weatherData.dates,
//             y: weatherData.precipitation,
//             type: 'bar',
//             name: 'precipitation',
//             marker: {color: 'rgb(0, 115, 195)'},
//             customdata: weatherData.prcp_cumulative,
//             hovertemplate: 'Date: %{x}<br>Precipitation: %{y} mm<br>Cumulative: %{customdata:.1f}<extra></extra>',
//         }], { title: 'Precipitation', hovermode: 'x unified' });
//     }
// });

document.getElementById('show_alerts').addEventListener('change', function(e){
    if (this.checked){
        Plotly.restyle('prcp-graph', {
            marker: {color: weatherData.colors_prcp}
        });
    } else {
        Plotly.restyle('prcp-graph', {
            marker: {color: 'rgb(0, 115, 195)'}
        });
    }
});

// document.addEventListener('DOMContentLoaded', () => {
//     const prcp_plot = document.getElementById('prcp-graph');
//     prcp_plot.on('plotly_click', function(e){
//         console.log(e);
//         alert('Clicked!');
//     });
// });

document.getElementById('weather-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    // console.log(formData);
    const variable = document.getElementById('variable-selector').value;
    const culture = document.getElementById('culture').value;
    document.getElementById('var-selector-title').style.display = 'block';

    fetch('get_weather_data/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        weatherData = {
            dates: data.dates,
            temp: {avg: data.avg_temp, max: data.max_temp, min: data.min_temp},
            rhum: {avg: data.avg_rhum, max: data.max_rhum, min: data.min_rhum},
            wspd: {avg: data.avg_wspd, max: data.max_wspd, min: data.min_wspd},
            precipitation: data.prcp,
            prcp_cumulative: data.prcp_cumulative,
            total_precipitation: data.prcp_total,
            alert_red: data.alert_red,
            alert_orange: data.alert_orange,
            alert_yellow: data.alert_yellow,
            colors_prcp: data.colors_prcp
        };

        // console.log(weatherData.colors_prcp);
        prcp_plot = document.getElementById('prcp-graph'),
        data = [{x:weatherData.dates, y:weatherData.precipitation, type:'bar',
        name: 'precipitation', marker:{color: weatherData.colors_prcp}, customdata: weatherData.prcp_cumulative,
        hovertemplate: 'Date: %{x}<br>Precipitation: %{y} mm<br>Cumulative: %{customdata:.1f}<extra></extra>'}],
        layout = {hovermode:'x unified',
        title: {text: 'Precipitation'}};

        // Plotly.newPlot('prcp-graph', [{
        //     x: weatherData.dates,
        //     y: weatherData.precipitation,
        //     type: 'bar',
        //     name: 'precipitation',
        //     marker: {color: weatherData.colors_prcp},
        //     customdata: weatherData.prcp_cumulative,
        //     hovertemplate: 'Date: %{x}<br>Precipitation: %{y} mm<br>Cumulative: %{customdata:.1f}<extra></extra>',
        // }], { title: 'Precipitation', 
        //     hovermode: 'x unified'
        // }, {showTips: false});

        Plotly.newPlot('prcp-graph', data, layout).then(()=>{
            prcp_plot.on('plotly_relayout', function(event){
                console.log(event);
                // alert('Clicked');
            })
        });

        var max = {
            x: weatherData.dates,
            y: weatherData[variable]['max'],
            type: 'scatter',
            name: 'Max', //variable.charAt(0).toUpperCase() + variable.slice(1) + ' Max',
            line: {dash: 'dot', width: 1, color: colors_variable[variable]['max']},
            visible: 'legendonly',
            hovertamplate: ''
        };
        var min = {
            x: weatherData.dates,
            y: weatherData[variable]['min'],
            type: 'scatter',
            name: 'Min', //variable.charAt(0).toUpperCase() + variable.slice(1) + 
            line: {dash: 'dot', width: 1, color: colors_variable[variable]['min']},
            visible: 'legendonly',
            hovertamplate: ''
        };
        var avg = {
            x: weatherData.dates,
            y: weatherData[variable]['avg'],
            type: 'scatter',
            name: 'Avg', //variable.charAt(0).toUpperCase() + variable.slice(1) 
            line: {color: colors_variable[variable]['avg']},
            hovertamplate: ''
        };

        document.getElementById('show_alerts').checked = true;
        // console.log(document.getElementById('show_alerts').checked);


        Plotly.newPlot('other-graph', [max, avg, min], { title: names_from_variable[variable], hovermode: 'x unified' }, {showTips: false});

        // const total = document.getElementById("prcp-total");
        // total.style.display = `Total Precipitation: ${weatherData.total_precipitation} mm` ? 'block' : 'none';

        if (weatherData.total_precipitation){
            document.getElementById("prcp-total").innerText = `Total Precipitation: ${weatherData.total_precipitation} mm`;
            document.getElementById("prcp-total").style.display = 'block';
            document.getElementById("show_alerts").style.display = 'block';
            document.getElementById("show_alerts_text").style.display = 'block';
        }

        // Update alert boxes if they exist
        ['red', 'orange', 'yellow'].forEach(color => {
            const box = document.getElementById(`alert-${color}`);
            const content = weatherData[`alert_${color}`];
            box.style.display = content ? 'block' : 'none';
            box.innerText = content || '';
        });
    });
});