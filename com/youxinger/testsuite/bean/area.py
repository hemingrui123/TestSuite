from com.youxinger.testsuite.bean.i_validate import IDataVerify
from com.youxinger.testsuite.bean.store import Store


class AreaVerifyData(object):
    """
    大区数据验证类
    """
    f_area_sales_amount = 0  # 大区销售额


class Area(IDataVerify):
    """
    大区
    """
    area_name = ''  # 大区编号
    area_id = ''  # 大区id
    stores: [Store] = None  # 要验证的门店列表
    preVerifyData: AreaVerifyData = None  # 操作前数据
    postVerifyData: AreaVerifyData = None  # 操作后数据
    expectedData: AreaVerifyData = None  # 期待增加值

    def __init__(self, area_name, area_id):
        self.area_name = area_name
        self.area_id = area_id
        self.preVerifyData = AreaVerifyData()
        self.postVerifyData = AreaVerifyData()

    def update_pre_verify_data(self):
        """
        更新操作之前的数据
        :return:
        """
        from com.youxinger.testsuite.service import financial_data_service
        financial_data_service.get_update_area_data(self.area_id, self.preVerifyData)
        if self.stores is not None:
            for store in self.stores:
                store.update_pre_verify_data()

    def update_post_verify_data(self):
        """
        更新操作之后的数据
        :return:
        """
        from com.youxinger.testsuite.service import financial_data_service
        financial_data_service.get_update_area_data(self.area_id, self.postVerifyData)
        if self.stores is not None:
            for store in self.stores:
                store.update_post_verify_data()

    def data_verify(self):
        if self.expectedData is not None:
            assert abs(
                self.postVerifyData.f_area_sales_amount - self.expectedData.f_area_sales_amount - self.preVerifyData.f_area_sales_amount) < 0.02, \
                "大区销售额检测失败,期待增加值:%d, 当前值:%d, 之前值:%d" % (
                    self.expectedData.f_area_sales_amount, self.postVerifyData.f_area_sales_amount, self.preVerifyData.f_area_sales_amount)

        if self.stores is not None:
            for store in self.stores:
                store.data_verify()