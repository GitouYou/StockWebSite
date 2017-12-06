

var index = $("#index_select option:selected").val()
var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var option = null;

myChart.showLoading();

function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data[i - j][1];
        }
        result.push(sum / dayCount);
    }
    return result;
}

function Paint(rawstr){

    var rawData = JSON.parse(rawstr);


    var dates = rawData.map(function (item) {
       return item[0];
    });


    var data = rawData.map(function (item) {
       return [+item[1], +item[2], +item[4], +item[3]];
    });


    myChart.hideLoading();
    option = {
    backgroundColor: '#21202D',
    legend: {
        data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30'],
        inactiveColor: '#777',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false,
            type: 'cross',
            lineStyle: {
                color: '#376df4',
                width: 2,
                opacity: 1
            }
        }
    },
    xAxis: {
        type: 'category',
        data: dates,
        axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
        scale: true,
        axisLine: { lineStyle: { color: '#8392A5' } },
        splitLine: { show: false }
    },
    grid: {
        bottom: 80
    },
    dataZoom: [{
        textStyle: {
            color: '#8392A5'
        },
        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        dataBackground: {
            areaStyle: {
                color: '#8392A5'
            },
            lineStyle: {
                opacity: 0.8,
                color: '#8392A5'
            }
        },
        handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
            shadowOffsetX: 2,
            shadowOffsetY: 2
        }
    }, {
        type: 'inside'
    }],
    animation: false,
    series: [
        {
            type: 'candlestick',
            name: '日K',
            data: data,
            itemStyle: {
                normal: {
                    color: '#FD1050',
                    color0: '#0CF49B',
                    borderColor: '#FD1050',
                    borderColor0: '#0CF49B'
                }
            }
        },
        {
            name: 'MA5',
            type: 'line',
            data: calculateMA(5, data),
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MA10',
            type: 'line',
            data: calculateMA(10, data),
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MA20',
            type: 'line',
            data: calculateMA(20, data),
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MA30',
            type: 'line',
            data: calculateMA(30, data),
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        }
    ]
};;

     myChart.setOption(option, true);


}
function IndexChange(changedindex){

    $.getJSON('/finweb/get_index_data/',{'index':changedindex},Paint);
    $('#index_name').html($("#index_select option:selected").text());

}

function Refresh(){
     $.getJSON('/finweb/get_span_data/',{'index':index},function(ret){
              console.trace(ret);
              console.trace(ret.change);
              $('#now').html("实时:"+ret.now);
              $('#change').html("涨跌:"+ret.change);
              $('#percent').html("幅度:"+ret.percent+'%');
              $('#volumn').html("成交量:"+ret.volumn+"亿");
              $('#amount').html("成交额:"+ret.amount+"亿");
              if(ret.change > 0 )
               {
                 $("#now").attr("style","color:#C03");
                 $("#change").attr("style","color:#C03");
                 $("#percent").attr("style","color:#C03");
               }
               else
               {
                  $("#now").attr("style","color:#00DB00");
                  $("#change").attr("style","color:#00DB00");
                  $("#percent").attr("style","color:#00DB00");

               }

          });
}

$.getJSON('/finweb/get_index_data/',{'index':index},Paint);;


 setInterval("Refresh()",800);



if (option && typeof option === "object") {

    myChart.setOption(option, true);
}

