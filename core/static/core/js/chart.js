$(document).ready(function(){
    drawChart();
});

function drawChart(){
    const ctx = $('#myChart');
    const stats_stuff = $('#stats_stuff');
    var ajax_data = [];
    var chart_labels = [];

    $.ajax({
        url: '/get_issue_data',
        dataType: 'json',
        async: false,
        cache: false,
        success: function (data) {
            let result = data.severity_totals;
            ajax_data = Object.keys(result).map((key) => result[key]);
            chart_labels = Object.keys(result);
        }
    });

    stats_stuff.append(`
        <table>
            <tr>
                <td>Severity</td>
                <td>Number</td>
            </tr>
            <tr>
                <td>${chart_labels[0]}</td>
                <td>${ajax_data[0]}</td>
            </tr>
            <tr>
                <td>${chart_labels[1]}</td>
                <td>${ajax_data[1]}</td>
            </tr>
            <tr>
                <td>${chart_labels[2]}</td>
                <td>${ajax_data[2]}</td>
            </tr>
            <tr>
                <td>${chart_labels[3]}</td>
                <td>${ajax_data[3]}</td>
            </tr>
            <tr>
                <td>${chart_labels[4]}</td>
                <td>${ajax_data[4]}</td>
            </tr>
            <tr>
                <td>Total</td>
                <td>${sum(ajax_data)}</td>
            </tr>
        </table>
    `);

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chart_labels,
            datasets: [{
                label: 'Vulnerability Stats',
                data: ajax_data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    gridLines: {
                        display:false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display:false
                    }
                }]
            }
        }
    });
}