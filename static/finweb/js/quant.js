//页面加载好时，获得select选中的组合名，显示组合中的股票列表信息


if(document.getElementById("portfolio_select"))
{
   var port_name = $("#portfolio_select option:selected").val();
   $.getJSON('/finweb/get_quant_data/',{'port_name':port_name},function(ret){

            $('#container').html('');

            $.each(ret, function(index, item){

                $('#container').append('<tr><td><span>'+ item.name +'</span></td>	 <td><span>'+ item.close+'</span></td> <td><span>'+ item.pb +'</span></td><td><span>'+ item.profits_yoy +'</span></td> <td><span>'+ item.targ+'</span></td>	<td><span>'+ item.nav +'</span></td>	<td><span>'+ item.mbrg+'</span></td>	<td><span>'+ item.nprg +'</span></td>	<td><span>'+ item.epsg +'</span></td></tr>');

            })
          });
}

function port_change(port_name){

    $.getJSON('/finweb/get_quant_data/',{'port_name':port_name},function(ret){

            $('#container').html('');

            $.each(ret, function(index, item){

                $('#container').append('<tr><td><span>'+ item.name +'</span></td>	<td><span>'+ item.close+'</span></td>	<td><span>'+ item.pb +'</span></td><td><span>'+ item.profits_yoy +'</span></td> <td><span>'+ item.targ+'</span></td>	<td><span>'+ item.nav +'</span></td>	<td><span>'+ item.mbrg+'</span></td>	<td><span>'+ item.nprg +'</span></td>	<td><span>'+ item.epsg +'</span></td></tr>');
            })
          });

}



