//指标解释文字的更新
//当select改变时刷新当前页面
var time = $("#select option:selected").val();


  $.get("/finweb/get_macd", {'time':time}, function(ret){
            $('#panel_m').html('') //清空前面的结果

            $.each(ret, function(index, item){
                $('#panel_m').append('<img src="/static/finweb/pics/'+ item+'">');
            })


        })

 $("#macd").click(function(){

        time = $("#select option:selected").val();
        $.get("/finweb/get_macd", {'time':time}, function(ret){
            $('#panel_m').html(''); //清空前面的结果
            $.each(ret, function(index, item){
                $('#panel_m').append('<img src="/static/finweb/pics/'+ item+'">');
            })

        })
     });

$("#adx").click(function(){

        time = $("#select option:selected").val();

        $.get("/finweb/get_adx",{'time':time}, function(ret){

           $('#panel_a').html(''); //清空前面的结果
           $.each(ret, function(index, item){
                $('#panel_a').append('<img src="/static/finweb/pics/'+ item+'">');
            })

        })
     });

$("#sma").click(function(){

        time = $("#select option:selected").val();
        $.get("/finweb/get_sma", {'time':time}, function(ret){
            $('#panel_s').html('') //清空前面的结果

            $.each(ret, function(index, item){
                $('#panel_s').append('<img src="/static/finweb/pics/'+ item+'">');
            })

        })
     });


$("#bbands").click(function(){

        time = $("#select option:selected").val();
        $.get("/finweb/get_bbands", {'time':time}, function(ret){
            $('#panel_b').html('') //清空前面的结果

             $.each(ret, function(index, item){
                $('#panel_b').append('<img src="/static/finweb/pics/'+ item+'">');
            })

        })
     });
