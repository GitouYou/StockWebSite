//切换到k线图时配置echarts  点击 ok
//分时图 的更新 当处于活跃时 ok
//span实时更新 ok
//加入自选
//取消自选 ok
//加入投资组合 ok
//点击搜索按钮 ok
//分时图的实时刷新

 var dom = document.getElementById("container");
 var myChart = echarts.init(dom);
 var option = null;

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

function Refresh(){
     //改变颜色，获取数据price.percent,updown,high,low
     $.getJSON('/finweb/get_info_stockdata/',function(ret){
          // 把 ret 的每一项显示在网页上
              $("span.price").html(ret.price)
              $("span.percent").html(ret.percent)
              $("span.updown").html(ret.updown)
              $("span.high").html(ret.high)
              $("span.low").html(ret.low)
               if(ret.updown >= 0 )
               {
                 $("span.color").attr("style","color:#C03");
               }
               else
               {
                  $("span.color").attr("style","color:#00DB00");

               }
               if(ret.high_red)
               {
                   $("span.color_high").attr("style","color:#C03");
               }
               else
               {
                  $("span.color_high").attr("style","color:#00DB00");
               }
               if(ret.low_red)
               {
                   $("span.color_low").attr("style","color:#C03");
               }
               else
               {
                  $("span.color_low").attr("style","color:#00DB00");
               }


          });
      var src = $("#day_pic").attr('src');
      $("#day_pic").attr('src',src);
}
setInterval("Refresh()",1000);


 $("#k_chart").click(function(){

    myChart.showLoading();
    $.getJSON('/finweb/get_info_kdata/',Paint);
 });


 $("#add").click(function(){

        var code = $(this).val();
        var portfolio = $("#portfolio_select option:selected").val();

        $.getJSON('/finweb/add_stocks_toport/',{'list_str':code,'portfolio':portfolio},function(ret){

              if(ret.result)
              {
                 alert('成功添加到'+$("#portfolio_select option:selected").text());

              }
        });
 });

 $("#search_btn").click(function(){

        var code = $("#code_input").val();

        $.getJSON('/finweb/get_info_search/',{'code':code},function(ret){
              if(ret.result){

                window.location.reload();
              }
              else
              {

                  alert("股票代码错误或暂不支持");
              }
        });
 });




$("#delete_info_stock").click(function(){
	   var code = $(this).val();
        $.getJSON('/finweb/delete_stocks/',{'list_str':code},function(ret){
              if(ret.result)
              {
                 window.location.reload();
               }
        });
 });


 $("#add_info_stock").click(function(){
	   var code = $(this).val();
        $.getJSON('/finweb/addto_stocks/',{'code':code},function(ret){
              if(ret.result)
              {
                 window.location.reload();
               }
        });
 });


