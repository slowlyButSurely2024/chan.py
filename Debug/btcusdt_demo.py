from Chan import CChan
from ChanConfig import CChanConfig
from Common.CEnum import KL_TYPE, DATA_SRC
from Plot.PlotDriver import CPlotDriver

# 配置缠论计算参数
config = CChanConfig({"bi_strict": True})

# 创建CChan实例
chan = CChan(
    code="btcusdt",  # 注意这里使用生成的CSV文件名前缀
    begin_time="2023-01-01",
    end_time=None,
    data_src=DATA_SRC.CSV,  # 使用CSV数据源
    lv_list=[KL_TYPE.K_60M],  # 或其他时间周期
    config=config,
)

plot_config = {
    "plot_kline": True,
    "plot_kline_combine": True,
    "plot_bi": True,
    "plot_seg": True,
    "plot_eigen": False,
    "plot_zs": True,
    "plot_macd": True,
    "plot_mean": False,
    "plot_channel": False,
    "plot_bsp": True,
    "plot_extrainfo": False,
    "plot_demark": False,
    "plot_marker": False,
    "plot_rsi": False,
    "plot_kdj": False,
}

plot_para = {
    "seg": {
        # "plot_trendline": True,
    },
    "bi": {
        # "show_num": True,
        # "disp_end": True,
    },
    "figure": {
        "x_seg_cnt": 10,
    },
    "marker": {
        # "markers": {  # text, position, color
        #     '2023/06/01': ('marker here', 'up', 'red'),
        #     '2023/06/08': ('marker here', 'down')
        # },
    }
}

plot_driver = CPlotDriver(chan, plot_config=plot_config)
plot_driver.figure.show()


# 创建并显示图表
plot_driver = CPlotDriver(
    chan,
    plot_config=plot_config,
    plot_para=plot_para,
)
plot_driver.figure.show()

# 保存图表
output_file = "./btcusdt_chan_demo.png"
plot_driver.save2img(output_file)