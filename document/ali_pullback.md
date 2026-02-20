<!--------------------------------------------------------------------------------- Description --->
# Poolback 4x4
```
Ichimoku Dual Cloud Switch Backtest
```
```
استراتژی پولبک ۴ برابر  
مبتنی بر دو ابر ایچیموکو – تریگر سویچ کومو در تنظیمات استاندارد + فیلتر روند در تنظیمات بزرگ‌تر
```
```
 جهت‌گیری اصلی: دنباله‌رو روند بزرگ (ابر Ichi2) + پولبک کوتاه‌مدت (سویچ ابر Ichi1)
```
```
واحد محاسبه pnl: تفاوت قیمت خام (بدون در نظر گرفتن حجم معامله، اسپرد، کمیسیون یا اسلیپیج)
```



<!--------------------------------------------------------------------------------- Parameters --->
<br><br>

## Parameters

<!----------------name--->
#### name
این پارامتر برای تعیین نام استراتژی می‌باشد
```
این پارامتر برای تعیین نام استراتژی می‌باشد
```
```python
name='poolback_4x'
```
<!----------------time_frame--->
#### time_frame
```
تایم‌فریم
```
```python
time_frame='m1'
```
<!----------------region--->
#### region
```
برای تعیین نوع تایم می‌باشد
```
```python
region='UTC'
```
<!----------------time_from--->
#### time_from
```
زمان شروع مجاز معامله
```
```python
time_from='00:00:00'
```
<!----------------time_to--->
#### time_to
```
زمان پایان مجاز معامله
```
```python
time_to='21:00:00'
```
<!----------------max_order--->
#### max_order
```
حداکثر پوزیشن همزمان
```
```python
max_order=1
```
<!----------------domain--->
#### domain
```
گرفتن های و لو همه آیتم‌های داخل متغیر پریود برای دومین دامنه گذشته
```
```python
domain=10
```
<!----------------period--->
#### period
```
تعداد کندل دوره‌های مختلف که کندل بر اساس متغیر تایم فریم تعیین می‌شود
```
```python
period = {
    "t1": 9,
    "k1": 26,
    "sb1": 78,
    "t2": 36,
    "k2": 104,
    "sb2": 234
}
```
<!----------------python--->
#### python
```python
params="{'name': 'poolback_4x', 'time_frame': 'm1', 'region': 'UTC', 'time_from': '00:00:00', 'time_to': '21:00:00', 'max_order': 1, 'domain': 10, 'period': {'t1': 9, 'k1': 26, 'sb1': 78, 't2': 36, 'k2': 104, 'sb2': 234}}"
```



<!--------------------------------------------------------------------------------- Actions --->
<br><br>

## Actions

<!----------------average--->
#### average
```
گرفتن های و لوی همه آیتم‌های داخل متغیر پریود
```
```python
average = {}
average_date = date
for i in range(10, 0, -1):
    average_item = {}
    #---average
    for key, value in self.period.items():
        high, low = self.box(date=average_date, count=value, time_frame=self.time_frame)
        average_item[key] = {"high": high, "low": low , "average": (high+low)/2}
    #---sa
    average_item['sa1'] = (average_item['t1']['average'] + average_item['k1']['average']) / 2
    average_item['sa2'] = (average_item['t2']['average'] + average_item['k2']['average']) / 2
    average[i] = average_item
    average_date = average_date - timedelta(minutes=1)
```

<!----------------tk--->
#### tk
```
tk
```
```python
if average[self.domain]['t2']['average'] > average[self.domain]['k2']['average'] :
    tk_up = True
    tk_down = False
else:
    tk_up = False
    tk_down = True
```

<!----------------kumo--->
#### kumo
```
kumo
```
```python
if average[self.domain]['sa2'] > average[self.domain]['sb2']['average'] :
    kumo_up = True
    kumo_down = False
else:
    kumo_up = False
    kumo_down = True
```
<!----------------switch_down--->
#### switch_down
```
switch_down
```
```python
if ask < average[self.domain]['sa1'] and ask < average[self.domain]['sb1']['average']:
    if average[self.domain]['sa1'] < average[self.domain]['sb1']['average']:
        point_avg_1 = average[self.domain]['sa1']
        point_avg_2 = average[self.domain]['sb1']['average']
        #---Live Big
        if point_avg_1 > point_avg_2 :
            switch_down = inner(self.domain)
```



<!--------------------------------------------------------------------------------- Methods --->
<br><br>

## Methods
<!----------------box--->

#### box
```
این متد یک دیت می‌گیرد یک عدد می‌گیرد و یک تایم فریم می‌گیرد و های و لو آن بازه را برای ما برمی‌گرداند
```
```python
def box(
        self,
        date:int, 
        count:int,
        time_frame:str,
    ):
    #--------------Description
    # IN     : date | count | time_frame
    # OUT    : high | low
    # Action : این متد یک دیت می‌گیرد یک عدد می‌گیرد و یک تایم فریم می‌گیرد و های و لو آن بازه را برای ما برمی‌گرداند
    #--------------Action
    table = get_tbl_name(self.symbol, self.time_frame)
    date_to = date
    date_from = date - timedelta(minutes=count)
    cmd = f"SELECT MAX(askhigh), MIN(asklow) FROM {table} WHERE date>='{date_from}' and date<='{date_to}'"
    result = self.data_sql.db.items(cmd=cmd).data
    high = result[0][0]
    low = result[0][1]
    return high, low
```