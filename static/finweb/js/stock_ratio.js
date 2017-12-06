$("#ratio_result").hide();
var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var option = null;
function Paint_Returns(return_str) {

   var returns = JSON.parse(return_str);
   var dates = returns.map(function (item) {
       return item[0];
    });
   var sharpe_data = returns.map(function (item) {
       return item[1];
    });
   var variance_data = returns.map(function (item) {
       return item[2];
    });

   option = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['夏普最优','风险最小']
    },
    toolbox: {
        show : true,
        feature : {
          dataZoom : {show: true},
        }
    },
    calculable : true,
    dataZoom : {
        show : true,
        realtime : true,
        start : 0,
        end : 100
    },
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : dates
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'夏普最优',
            type:'line',
            data: sharpe_data
        },
        {
            name:'风险最小',
            type:'line',
            data: variance_data
        }
    ]
};
  myChart.setOption(option, true);

}

$("#datetimeStart").datetimepicker({
        format: 'yyyy-mm-dd',
        minView:'month',
        language: 'zh-CN',
        autoclose:true,
        endDate:new Date()
    }).on('changeDate', function(ev){

            if(ev.date){
                $("#datetimeEnd").datetimepicker('setStartDate', new Date(ev.date.valueOf()));
            }else{
                $("#datetimeEnd").datetimepicker('setStartDate',null);
            }
          })  ;

    $("#datetimeEnd").datetimepicker({
        format: 'yyyy-mm-dd',
        minView:'month',
        language: 'zh-CN',
        autoclose:true,
        todayHighlight:true,
        todayBtn:true,
        endDate:new Date()
    }).on('changeDate', function(ev){

            if(ev.date){
                $("#datetimeStart").datetimepicker('setEndDate', new Date(ev.date.valueOf()));
            }else{
                $("#datetimeStart").datetimepicker('setEndDate',new Date());
            }

          }) ;

//用户点击资产配置分析按钮，
//检查输入是否为空
//得到投资比例建议
$("#ratio_btn").click(function(){

     var from = $("#input_from").val();
     var to = $("#input_to").val();

     if( from == '' || to== '')
     {
        if( from == ''){
           alert("请选择起始日期");
        }
        if( to == ''){
           alert("请选择结束日期");
        }
     }else{

       $.getJSON('/finweb/get_stock_ratio/',{'from':from,'to':to},function(ret){

            $("#ratio_result").show();
            $("#sharpe").html('');
            $("#variance").html('');
            for(var i=0;i<ret.stock_list.length;i++){

                $('#sharpe').append('<tr><td><span>'+ ret.stock_list[i] +'</span></td>	 <td><span>'+ ret.name_list[i]+'</span></td> <td><span>'+ ret.price_list[i] +'</span></td> <td><span>'	+ ret.sharpe_ratio[i] +'</span></td></tr>');
                $('#variance').append('<tr><td><span>'+ ret.stock_list[i] +'</span></td>	 <td><span>'+ ret.name_list[i]+'</span></td> <td><span>'+ ret.price_list[i]+'</span></td> <td><span>'	+ ret.variance_ratio[i] +'</span></td></tr>');

             }
              $('#s_exp_return').html("预期收益率:"+ret.sharpe_result[0]);
              $('#s_exp_variance').html("预期波动率:"+ret.sharpe_result[1]);
              $('#s_sharpe').html("夏普指数:"+ret.sharpe_result[2]);

               $('#v_exp_return').html("预期收益率:"+ret.variance_result[0]);
               $('#v_exp_variance').html("预期波动率:"+ret.variance_result[1]);
               $('#v_sharpe').html("夏普指数:"+ret.variance_result[2]);

               Paint_Returns(ret.return_str);

          });



     }
});
