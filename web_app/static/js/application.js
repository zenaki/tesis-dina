var sound_value = null;
var gsr_value = null;
var chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

$(document).ready(function() {
    //connect to the socket server.
    var ws = new WebSocket("ws://"+window.location.hostname+":1234");
    ws.onmessage = function(event) {
        console.log("Get Data: " + event.data);
        sound_value = parseInt(JSON.parse(event.data).data_sound);
        gsr_value = parseInt(JSON.parse(event.data).data_gsr);
    };

    drawChartSound();
    drawChartGSR();
});

function drawChartSound() {
    var color = Chart.helpers.color;
    var config = {
        type: 'line',
        data: {
            datasets: [{
                label: '',
                backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
                borderColor: chartColors.blue,
                fill: false,
                cubicInterpolationMode: 'monotone',
                data: []
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Sound'
            },
            scales: {
                xAxes: [{
                    type: 'realtime',
                    realtime: {
                        duration: 6000,
                        refresh: 0.1,
                        delay: 0.1,
                        onRefresh: onRefreshSound
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'value'
                    }
                }]
            },
            tooltips: {
                mode: 'nearest',
                intersect: false
            },
            hover: {
                mode: 'nearest',
                intersect: false
            }
        }
    };

    var ctx = document.getElementById('SoundChart').getContext('2d');
    window.SoundChart = new Chart(ctx, config);
}

function onRefreshSound(chart) {
    // console.log('sound_value', sound_value);
    chart.config.data.datasets.forEach(function(dataset) {
        dataset.data.push({
            x: Date.now(),
            // y: randomScalingFactor()
            y: sound_value
        });
    });
}

function drawChartGSR() {
    var color = Chart.helpers.color;
    var config = {
        type: 'line',
        data: {
            datasets: [{
                label: 'microsiemens',
                backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
                borderColor: chartColors.blue,
                fill: false,
                cubicInterpolationMode: 'monotone',
                data: []
            }]
        },
        options: {
            title: {
                display: true,
                text: 'GSR Sensor'
            },
            scales: {
                xAxes: [{
                    type: 'realtime',
                    realtime: {
                        duration: 6000,
                        refresh: 0.1,
                        delay: 0.1,
                        onRefresh: onRefreshGSR
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'value'
                    }
                }]
            },
            tooltips: {
                mode: 'nearest',
                intersect: false
            },
            hover: {
                mode: 'nearest',
                intersect: false
            }
        }
    };

    var ctx = document.getElementById('GSRChart').getContext('2d');
    window.GSRChart = new Chart(ctx, config);
}

function onRefreshGSR(chart) {
    chart.config.data.datasets.forEach(function(dataset) {
        dataset.data.push({
            x: Date.now(),
            // y: randomScalingFactor()
            y: gsr_value
        });
    });
}

function randomScalingFactor() {
    return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 10);
}