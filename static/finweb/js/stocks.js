// color 类改变颜色
// color_high 类改变颜色
// color_high 类改变颜色
//change 类实时更新
// checked 删除自选股
//添加到投资组合
//name类点击设置session跳转到个股信息页面

function Refresh(){
     //改变颜色，获取数据price.percent,updown,high,low
     $.getJSON('/finweb/get_stocks_data/',function(ret){
//              console.trace(ret);
//              console.trace(ret.change);
              for (var i = ret.length - 1; i >= 0; i--) {
              // 把 ret 的每一项显示在网页上
              $('#'+ ret[i].code).find("span.price").html(ret[i].price)
              $('#'+ ret[i].code).find("span.percent").html(ret[i].percent)
              $('#'+ ret[i].code).find("span.updown").html(ret[i].updown)
              $('#'+ ret[i].code).find("span.high").html(ret[i].high)
              $('#'+ ret[i].code).find("span.low").html(ret[i].low)
               if(ret[i].updown >= 0 )
               {
                 $('#'+ ret[i].code).find("span.color").attr("style","color:#C03");
               }
               else
               {
                  $('#'+ ret[i].code).find("span.color").attr("style","color:#00DB00");

               }
               if(ret[i].high_red)
               {
                   $('#'+ ret[i].code).find("span.color_high").attr("style","color:#C03");
               }
               else
               {
                  $('#'+ ret[i].code).find("span.color_high").attr("style","color:#00DB00");
               }
               if(ret[i].low_red)
               {
                   $('#'+ ret[i].code).find("span.color_low").attr("style","color:#C03");
               }
               else
               {
                  $('#'+ ret[i].code).find("span.color_low").attr("style","color:#00DB00");
               }
            };

          });
}
setInterval("Refresh()",3000);


$(".name").click(function(){

      var code = $(this).parents("tr").attr('id')
     $.getJSON('/finweb/stocks_to_info/',{'code':code},function(ret){
              if(ret.result){
                  window.location.href="../stockinfo";
              }
         });
});

$("#all_none").click(function(){
      if ($(this).text() == "全选"){
            $(this).text("全不选");
            $(".box").prop('checked',true);
      }
      else if($(this).text() == "全不选"){
            $(this).text("全选");
            $(".box").prop('checked',false);
      }
});


$("#delete").click(function(){
		var valArr = new Array;
		//获取选中选项的值
        $("input:checkbox[name='code_list']:checked").each(function(i){
			valArr[i] = $(this).val();
//			console.trace($(this).val());
        });
		var vals = ''
		vals = valArr.join(';');
//		alert(vals);
        $.getJSON('/finweb/delete_stocks/',{'list_str':vals},function(ret){
              if(ret.empty){
                 alert('没有选择任何股票！');
              }
              else if(ret.result)
              {
                 window.location.reload();
              }
        });
 });

 $("#add").click(function(){
		var valArr = new Array;
		var portfolio = $("#portfolio_select option:selected").val();
        $("input:checkbox[name='code_list']:checked").each(function(i){
			valArr[i] = $(this).val();
        });
		var vals = ''
		vals = valArr.join(';');
        $.getJSON('/finweb/add_stocks_toport/',{'list_str':vals,'portfolio':portfolio},function(ret){
              if(ret.empty){
                 alert('没有选择任何股票！');
              }
              else if(ret.result)
              {
                 alert('成功添加到'+$("#portfolio_select option:selected").text());
                 $(".box").prop('checked',false);
              }
        });
 });

