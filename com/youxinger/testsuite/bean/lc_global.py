from com.youxinger.testsuite.bean.area import Area, AreaVerifyData
from com.youxinger.testsuite.bean.i_validate import IDataVerify
from com.youxinger.testsuite.bean.repository import Repository
import logging


class LCGlobalVerifyData(object):
    """
    总览验证数据
    """
    i_lc_global_arrive_store_num = 0  # 总揽到店次数
    f_lc_global_bhm_percent = 0.0  # 总揽测量成单率
    i_lc_global_newvip_num = 0  # 总揽新增会员数
    f_lc_global_newvip_order_percent = 0.0  # 总揽新会员成单率
    i_lc_global_order_num = 0  # 总揽订单数
    i_lc_global_refund_num = 0  # 总揽退单数
    f_lc_global_sale_num = 0.0  # 总揽销售总额
    f_lc_global_sale_percent = 0.0  # 总揽销售完成比

    @classmethod
    def expected_data(cls, i_lc_global_arrive_store_num, i_lc_global_newvip_num, i_lc_global_order_num,
                      i_lc_global_refund_num, f_lc_global_sale_num):
        """
        创建预期值对象
        :param i_lc_global_arrive_store_num: 总揽到店次数
        :param i_lc_global_newvip_num: 总揽新增会员数
        :param i_lc_global_order_num: 总揽订单数
        :param i_lc_global_refund_num: 总揽退单数
        :param f_lc_global_sale_num: 总揽销售总额
        :return:
        """
        exp_value = cls()
        exp_value.i_lc_global_arrive_store_num = i_lc_global_arrive_store_num
        exp_value.i_lc_global_newvip_num = i_lc_global_newvip_num
        exp_value.i_lc_global_order_num = i_lc_global_order_num
        exp_value.i_lc_global_refund_num = i_lc_global_refund_num
        exp_value.f_lc_global_sale_num = f_lc_global_sale_num
        return exp_value


class LCGlobal(IDataVerify):
    """
    总览信息
    """
    areas: [Area] = None  # 要验证的大区列表
    repository: Repository = None  # 要验证的仓库
    preVerifyData: LCGlobalVerifyData = None  # 操作前数据
    postVerifyData: LCGlobalVerifyData = None  # 操作后数据
    expectedData: LCGlobalVerifyData = None  # 期待增加值

    def __init__(self, repository):
        self.preVerifyData = LCGlobalVerifyData()
        self.postVerifyData = LCGlobalVerifyData()
        self.repository = repository
        self.areas = []

    def update_expected_area_verify_data(self, expected_area_list):
        """
        更新期待大区验证值
        :return:
        """
        if expected_area_list is not None:
            for area in self.areas:
                area.expectedData = expected_area_list.get(area.area_id)

    def update_pre_verify_data(self):
        """
        更新操作之前的数据
        :return:
        """
        from com.youxinger.testsuite.service import financial_data_service
        financial_data_service.get_update_global_data(self.preVerifyData)
        self.repository.update_pre_verify_data()
        if self.areas is not None:
            for area in self.areas:
                area.update_pre_verify_data()

    def update_post_verify_data(self):
        """
        更新操作之后的数据
        :return:
        """
        from com.youxinger.testsuite.service import financial_data_service
        financial_data_service.get_update_global_data(self.postVerifyData)
        self.repository.update_post_verify_data()
        if self.areas is not None:
            for area in self.areas:
                area.update_post_verify_data()

    def data_verify(self):
        if self.expectedData is not None:
            assert abs(
                self.postVerifyData.i_lc_global_arrive_store_num - self.expectedData.i_lc_global_arrive_store_num - self.preVerifyData.i_lc_global_arrive_store_num) == 0, \
                "总揽到店次数检测失败,期待增加值:%d, 当前值:%d, 之前值:%d" % (
                    self.expectedData.i_lc_global_arrive_store_num, self.postVerifyData.i_lc_global_arrive_store_num, self.preVerifyData.i_lc_global_arrive_store_num)
            assert abs(
                self.postVerifyData.i_lc_global_newvip_num - self.expectedData.i_lc_global_newvip_num - self.preVerifyData.i_lc_global_newvip_num) == 0, \
                "总揽新增会员数检测失败,期待增加值:%d, 当前值:%d, 之前值:%d" % (
                    self.expectedData.i_lc_global_newvip_num, self.postVerifyData.i_lc_global_newvip_num, self.preVerifyData.i_lc_global_newvip_num)
            assert abs(
                self.postVerifyData.i_lc_global_order_num - self.expectedData.i_lc_global_order_num - self.preVerifyData.i_lc_global_order_num) == 0, \
                "总揽订单数检测失败,期待增加值:%d, 当前值:%d, 之前值:%d" % (
                    self.expectedData.i_lc_global_order_num, self.postVerifyData.i_lc_global_order_num, self.preVerifyData.i_lc_global_order_num)
            assert abs(
                self.postVerifyData.i_lc_global_refund_num - self.expectedData.i_lc_global_refund_num - self.preVerifyData.i_lc_global_refund_num) == 0, \
                "总揽退单数检测失败,期待增加值:%d, 当前值:%d, 之前值:%d" % (
                    self.expectedData.i_lc_global_refund_num, self.postVerifyData.i_lc_global_refund_num, self.preVerifyData.i_lc_global_refund_num)
            assert abs(
                self.postVerifyData.f_lc_global_sale_num - self.expectedData.f_lc_global_sale_num - self.preVerifyData.f_lc_global_sale_num) < 2, \
                "总揽销售总额检测失败,期待增加值:%d, 当前值:%f, 之前值:%f" % (
                    self.expectedData.f_lc_global_sale_num, self.postVerifyData.f_lc_global_sale_num, self.preVerifyData.f_lc_global_sale_num)
        else:
            logging.debug("LCGlobal无预期值，无需进行数据验证")

        if self.repository is not None:
            self.repository.data_verify()

        if self.areas is not None:
            for area in self.areas:
                area.data_verify()