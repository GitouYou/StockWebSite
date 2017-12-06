//全选、全不选
//删除股票

$("#all_none").click(function(){

      if ($(this).text() == "全选"){
            $(this).text("全不选");
            $("input").prop('checked',true);
      }
      else if($(this).text() == "全不选"){
            $(this).text("全选");
            $("input" ).prop('checked',false);

      }
});


$("#delete").click(function(){
		var valArr = new Array;
		var name = $(this).attr('value');
		//获取选中选项的值
        $("input:checkbox[name='code_list']:checked").each(function(i){
			valArr[i] = $(this).val();
        });
		var vals = ''
		vals = valArr.join(';');
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






