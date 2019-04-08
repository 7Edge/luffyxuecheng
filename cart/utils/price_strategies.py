#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: price_strategies
# Date: 4/8/2019
"""
参照策略模式，定义多种优惠券使用计算价格策略
"""


# Context 类， 包裹策略对象

class StrategyContext(object):

    def __init__(self, coupon_strategy):
        self.coupon_strategy = coupon_strategy

    def cashing(self, money):
        return self.coupon_strategy.get_cash(money)


# 优惠券策略抽象类

class BaseStrategy(object):
    def get_cash(self, money):
        raise NotImplementedError('%s.get_cash must be implemented.' % self.__class__.__name__)


class FullReductionStrategy(BaseStrategy):
    """
    满减策略
    """

    def __init__(self, boundary, reduce):
        """

        :param boundary: 满多少钱
        :param reduce: 减多少钱
        """
        self.boundary = boundary
        self.reduce = reduce

    def is_okay(self, money):
        """
        额外条件满足
        :return:
        """
        return True

    def get_cash(self, money):
        if money < self.boundary or not self.is_okay(money):
            return money

        return money - self.reduce


class LimitFullReductionStrategy(FullReductionStrategy):
    """
    有最低消费限制满减
    """

    def __init__(self, boundary, reduce, lowest_limit):
        self.lowest_limit = lowest_limit
        super().__init__(boundary=boundary, reduce=reduce)

    def is_okay(self, money):
        return money >= self.lowest_limit


class DiscountStrategy(BaseStrategy):

    def __init__(self, percent):
        self.percent = percent

    def is_okay(self, money):
        """
        额外条件满足
        :return:
        """
        return True

    def get_cash(self, money):
        if not self.is_okay(money):
            return money

        return money * self.percent * 0.01


class LimitDiscountStrategy(DiscountStrategy):
    """
    有限制的折扣
    """

    def __init__(self, percent, lowest_limit):
        self.lowest_limit = lowest_limit
        super().__init__(percent=percent)

    def is_okay(self, money):
        return money >= self.lowest_limit


class DirectReduceStrategy(BaseStrategy):
    """
    无条件立减
    """

    def __init__(self, direct_reduce):
        self.direct_reduce = direct_reduce

    def get_cash(self, money):
        money_after = money - self.direct_reduce
        return money_after if money_after >= 0 else 0


if __name__ == '__main__':
    pass
