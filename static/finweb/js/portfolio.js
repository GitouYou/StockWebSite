//全选、全不选 针对不同组合
//删除股票 删除组合
//name类点击设置session跳转到个股信息页面


$(".name").click(function(){

     var code = $(this).parents("tr").attr('id');
     $.getJSON('/finweb/port_to_info/',{'code':code},function(ret){
              if(ret.result){
                  window.location.href="../stockinfo";
              }
         });
});

$(".all_none").click(function(){
     var name = $(this).attr('title')
      if ($(this).text() == "全选"){
            $(this).text("全不选");
            $("input."+ name ).prop('checked',true);
      }
      else if($(this).text() == "全不选"){
            $(this).text("全选");
            $("input."+ name ).prop('checked',false);

      }
});


$(".delete_s").click(function(){
		var valArr = new Array;
		var name = $(this).attr('value');
		//获取选中选项的值
        $("input."+ name +":checkbox[name='code_list']:checked").each(function(i){
			valArr[i] = $(this).val();
//			console.trace($(this).val());
        });
		var vals = ''
		vals = valArr.join(';');
//		alert(vals + name);
        $.getJSON('/finweb/delete_stocks_inp/',{'list_str':vals,'name':name},function(ret){
              if(ret.empty){
                 alert('没有选择任何股票！');
              }
              else if(ret.result)
              {
                 window.location.reload();
              }
        });
 });


 $(".delete_p").click(function(){
		var name = $(this).attr('value');
//		alert(name);
        $.getJSON('/finweb/delete_portfolio/',{'name':name},function(ret){
              if(ret.result){
//                 alert('删除组合成功！');
                 window.location.reload();
              }

        });
 });



