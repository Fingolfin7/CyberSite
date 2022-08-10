$(document).ready(function(){
    drawChart();
});

function drawChart(){
    const ctx = $('#myChart');
    const stats_stuff = $('#stats_stuff');
    var ajax_data = [];
    var chart_labels = [];
    let id = $("#back").attr("href").split("/")[2];
    console.log(id);
    $.ajax({
        url: '/get_issue_data/' + id,
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
            <thead>
                <th>Severity</th>
                <th>Number</th>
            </thead>
            <tr>
                <td class="no-borders">${chart_labels[0]}</td>
                <td class="no-borders">${ajax_data[0]}</td>
            </tr>
            <tr>
                <td class="no-borders">${chart_labels[1]}</td>
                <td class="no-borders">${ajax_data[1]}</td>
            </tr>
            <tr>
                <td class="no-borders">${chart_labels[2]}</td>
                <td class="no-borders">${ajax_data[2]}</td>
            </tr>
            <tr>
                <td class="no-borders">${chart_labels[3]}</td>
                <td class="no-borders">${ajax_data[3]}</td>
            </tr>
            <tr>
                <td class="no-borders">${chart_labels[4]}</td>
                <td class="no-borders">${ajax_data[4]}</td>
            </tr>
            <tr>
                <td class="no-borders">Total</td>
                <td class="no-borders">${ajax_data.reduce(function(a, b) { return a + b; }, 0)}</td>
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
                    'rgba(255, 0, 0, 0.2)',
                    'rgba(255, 192, 0, 0.2)',
                    'rgba(255, 255, 0, 0.2)',
                    'rgba(0, 176, 80, 0.2)',
                    'rgba(0, 112, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 0, 0, 1)',
                    'rgba(255, 192, 0, 1)',
                    'rgba(255, 255, 0, 1)',
                    'rgba(0, 176, 80, 1)',
                    'rgba(0, 112, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = 0;
                        let dataArr = ctx.chart.data.datasets[0].data;
                        dataArr.map(data => {
                            sum += data;
                        });
                        let percentage = (value*100 / sum).toFixed(2)+"%";
                        return percentage;
                    },
                    color: '#fff',
                }
            },
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