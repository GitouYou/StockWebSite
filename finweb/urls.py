# -*- coding: utf-8 -*-
from django.conf.urls import patterns,url
from finweb import views

urlpatterns = patterns('',
             url(r'^$',views.index,name='index'),
             url(r'^register/$',views.register,name='register'),
             url(r'^login/$',views.user_login,name='login'),
             url(r'^rules/$',views.rules,name='rules'),
             url(r'^changepassword/$',views.changepassword,name='changepassword'),
             url(r'^changeinfo/$',views.changeinfo,name='changeinfo'),
             url(r'^logout/$',views.user_logout,name='logout'),
             url(r'^get_index_data/$',views.get_index_data,name='get_index_data'),
             url(r'^get_span_data/$',views.get_span_data,name='get_span_data'),
             url(r'^get_stocks_data/$',views.get_stocks_data,name='get_stocks_data'),
             url(r'^stocks_to_info/$',views.stocks_to_info,name='stocks_to_info'),
             url(r'^delete_stocks/$',views.delete_stocks,name='delete_stocks'),
             url(r'^add_stocks_toport/$',views.add_stocks_toport,name='add_stocks_toport'),
             url(r'^userinfo/$',views.userinfo,name='userinfo'),
             url(r'^quant/$',views.quant,name='quant'), #量化投资
             url(r'^operate/$',views.operate,name='operate'),#股票操作
             url(r'^stocks/$',views.stocks,name='stocks'),#我的自选股
             url(r'^portfolio/$',views.portfolio,name='portfolio'),#我的投资组合
             url(r'^add_portfolio/$',views.add_portfolio,name='add_portfolio'),#创建投资组合
             url(r'^port_to_info',views.port_to_info,name='port_to_info'),#跳转
             url(r'^delete_stocks_inp/$',views.delete_stocks_inp,name='delete_stocks_inp'),#删除组合中的股票
             url(r'^delete_portfolio/$',views.delete_portfolio,name='delete_portfolio'),#删除组合
             url(r'^stockinfo/$',views.stockinfo,name='stockinfo'),#个股信息页面
             url(r'^get_info_stockdata/$',views.get_info_stockdata,name='get_info_stockdata'),#个股信息页面上更新span
             url(r'^get_info_kdata/$',views.get_info_kdata,name='get_info_kdata'),#个股信息页面上获取k线数据
             url(r'^get_info_search/$',views.get_info_search,name='get_info_search'),#个股信息页面搜索
             url(r'^addto_stocks/$',views.addto_stocks,name='addto_stocks'),#个股信息,添加到自选股
             url(r'^indicator/$',views.indicator,name='indicator'),#技术指标
             url(r'^get_macd/$',views.get_macd,name='get_macd'), #获得MACD指标图像
             url(r'^get_adx/$',views.get_adx,name='get_adx'), #获得ADX指标图像
             url(r'^get_sma/$',views.get_sma,name='get_sma'), #获得SMA指标图像
             url(r'^get_bbands/$',views.get_bbands,name='get_bbands'), #获得BBands指标图像
             url(r'^get_quant_data/$',views.get_quant_data,name='get_quant_data'),#选择组合
             url(r'^factor_analysis/$',views.factor_analysis,name='factor_analysis'),#多因子分析
             url(r'^stock_ratio/$',views.stock_ratio,name='stock_ratio'), #资产配置
             url(r'^get_stock_ratio/$',views.get_stock_ratio,name='get_stock_ratio'),
             url(r'^revenue_test/$',views.revenue_test,name='revenue_test'),#收益回测
             url(r'^fin_data/$',views.fin_data,name='fin_data'),
             url(r'^notices/$',views.notices,name='notices'),
             url(r'^candle1/$',views.candle1,name='candle1'),#test
             url(r'^news_test/$',views.news_test,name='news_test'),#test
             url(r'^candle/$',views.candle,name='candle'),#test
             url(r'^echarts/$',views.echarts,name='echarts'), #test
             url(r'^test/$',views.test,name='test'), #test
            )
