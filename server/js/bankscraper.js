// Some global variables
var seriesOptions = [];
var seriesCounter = 0;
var account = '0312500050278659';
var category = [];
var cumulateTransactions = function (transactions) {
    var result = [];
    var last = 0;
    for (var i=0; i<transactions.length; i++) {
        last += transactions[i][3];
        result.push([new Date(transactions[i][0]).getTime(), last]);
    }
    return result;
};
// Th update function
var update = function () {
    // create the chart when all data is loaded
    var createChart = function () {
        $('#container').highcharts('StockChart', {
            rangeSelector: {
                selected: 4
            },
            yAxis: {
                labels: {
                    formatter: function () {
                        return (this.value > 0 ? ' + ' : '') + this.value;
                    }
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: 'silver'
                }]
            },
            plotOptions: {
                series: {
                    compare: 'value'
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
                valueDecimals: 2
            },        
            series: seriesOptions
        });
    };
    // Get the accounts
    $.getJSON('/api/category', function(categories) {
        categories.push(['null', 'uncategorized', '']);
        // Plot each account
        $.each(categories, function (i, category) {
            $.getJSON('/api/transaction?account_id='+account+'&category_id='+category[0],
                      function (transactions) {
                          // Setup series
                          seriesOptions[i] = {
                              name: category[1],
                              data: cumulateTransactions(transactions)
                          };
                          // As we're loading the data asynchronously, we don't know what order it will arrive. So
                          // we keep a counter and create the chart when all the data is loaded.
                          seriesCounter += 1;
                          // Finaly create the chart
                          if (seriesCounter === categories.length) {
                              createChart();
                          }
                      });
        });
    });
};
// Managing categories submitting
var check = function (transaction, category) {
    if (category) {
        $.get( '/api/transaction_category?q=insert&transaction='+transaction+'&category='+category, function( data ) {
            $('#'+transaction+'-checked').text(category)
            $('#'+transaction+'-checked').show();
            $('#'+transaction+'-unchecked').hide();
        });
    }
};
var uncheck = function (transaction) {
    $.get( '/api/transaction_category?q=delete&transaction='+transaction, function( data ) {
        $('#'+transaction+'-checked').hide();
        $('#'+transaction+'-unchecked').show();
    });
};
// /api/transaction_category?q=insert&transaction=21340&category=3
// Update after loading
$(function () {
    // First update
    update();
    // Then every hour
    window.setInterval(update, 3600000);
});
