
from prettytable import PrettyTable


class LifeStyleDietPlan:
    def __init__(self, gender, age, height_cm, weight_kg):
        self.gender = gender
        self.age = age
        self.height_cm = height_cm
        self.height_m = height_cm / 100
        self.weight_kg = weight_kg
        self.weight_g = weight_kg * 1000

    @property
    def BMI(self):
        ''' Body Mass Index, 身体质量指数
        停止有氧: <23  正常: 8.5-24  超重: 24-28  肥胖: >28
        '''
        return round(self.weight_kg / self.height_m ** 2, 1)

    @property
    def BMR(self):
        ''' Basal Metabolic Rate, 基础代谢率
        计算(Mifflin-St Jeor): 9.99*体重 + 6.25*身高 - 4.92*年龄 + 5
        '''
        return int(self.weight_kg * 9.99 + self.height_cm * 6.25 - self.age * 4.92 + 5)

    @property
    def TDEE(self):
        '''Total Daily Energy Expenditure, 每日总热量消耗
        估算: BMR/0.7
        '''
        return int(self.BMR / 0.7)

    @property
    def DAEE(self):
        '''Daily Aerobic Exercise Expenditure, 每日有氧训练消耗
        自行安排并执行: 一周消耗/7
        '''
        return 0

    @property
    def weight_change_rate(self):
        return 0.96

    def weight_kg_after_months(self, months):
        return round(self.weight_kg * self.weight_change_rate ** months, 1)

    @property
    def caloric_balance(self):
        """ 平衡热量 = 活动消耗 + 有氧消耗 """
        return self.TDEE + self.DAEE

    @property
    def caloric_intake(self):
        """摄入热量 = 平衡热量*0.8*0.8 [前0.8热量缺口, 后0.8防止多吃]"""
        return int(self.caloric_balance * 0.8 * 0.8)

    def export(self):
        table = PrettyTable()
        table.title = '个人身体数据 & 生活化减脂饮食方案 (@好人松松)'
        table.field_names = ['项目', '数值', '备注']
        table.add_row(['年龄', self.age, ''])
        table.add_row(['身高 (cm)', f'{self.height_cm}', ''])
        table.add_row(['体重 (kg)', f'{self.weight_kg}', '目标: 60~70'])
        table.add_row(['身体指数 (kg/m^2)', self.BMI, '停止有氧: <23  正常: 8.5-24  超重: 24-28  肥胖: >28'])
        table.add_row(['基础代谢 (kcal)', self.BMR, '计算(Mifflin-St Jeor): 9.99*体重 + 6.25*身高 - 4.92*年龄 + 5'])
        table.add_row(['每日消耗 (kcal)', self.TDEE, '估算: BMR/0.7'])
        table.add_row(['有氧消耗 (kcal)', self.DAEE, '自行安排并执行: 一周消耗/7'])
        table.add_row(['平衡热量 (kcal)', self.caloric_balance, '平衡热量 = 活动消耗 + 有氧消耗'])
        table.add_row(['摄入热量 (kcal)', self.caloric_intake, '摄入热量 = 平衡热量*0.8*0.8 [前0.8热量缺口, 后0.8防止多吃]'])
        table.add_row(['每月体重 (kg)', f'{self.weight_kg_after_months(1)}, {self.weight_kg_after_months(2)}, {self.weight_kg_after_months(3)}', f'体重变化率: {self.weight_change_rate}'])

        # table.float_format = ".2f"
        table.align['项目'] = 'l'
        table.align['备注'] = 'l'
        print(table)


def main():
    pdp = LifeStyleDietPlan('male', 32, 170, 80)

    pdp.export()

if __name__ == '__main__':
    main()
